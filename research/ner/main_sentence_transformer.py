import spacy
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
import json
from transformers import pipeline
# Use a pipeline as a high-level helper
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch 
from promp_text import text

# pipe = pipeline("text-generation", model="meta-llama/Llama-2-7b-hf")
pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load Sentence-BERT model for embeddings
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')



### Step 1: Extract Entities from Text
doc = nlp(text)
entities = []
for ent in doc.ents:
    # Only add entities that are commonly useful like PERSON, ORG, GPE (places), etc.
    if ent.label_ in ["PERSON", "ORG", "GPE"]:
        entities.append(ent.text)

# Remove duplicate entities
entities = list(set(entities))
print("entities:", entities)

### Step 2: Create Embeddings and Cluster Entities
# Generate embeddings for each entity using Sentence-BERT
embeddings = sbert_model.encode(entities)

# Cluster similar entities using Agglomerative Clustering
clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.0)
clusters = clustering_model.fit_predict(embeddings)

# Group entities by cluster labels
clustered_entities = {}
for i, label in enumerate(clusters):
    if label not in clustered_entities:
        clustered_entities[label] = []
    clustered_entities[label].append(entities[i])
print("clustered_entities:",clustered_entities)

### Step 3: Extract and Combine Context for Each Cluster
entity_descriptions = {}
for label, entity_group in clustered_entities.items():
    context_sentences = []
    for entity in entity_group:
        for sent in doc.sents:
            if entity in sent.text:
                context_sentences.append(sent.text)
    # Join context sentences into a single description
    description = " ".join(context_sentences)
    # Assign the description to the first entity as the key
    entity_descriptions[entity_group[0]] = description

### Step 4: Export to JSON Format
json_output = json.dumps(entity_descriptions, indent=4)
print(json_output)

# Optionally save to a file
with open("entity_descriptions.json", "w") as file:
    file.write(json_output)


import json
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained Sentence-BERT model for similarity scoring
model = SentenceTransformer('all-MiniLM-L6-v2')

import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the Llama 2 model and tokenizer from Hugging Face
# model_name = "meta-llama/Llama-2-7b-hf"  # Choose "Llama-2-13b-hf" if you have more resources
model_name = "meta-llama/Llama-3.2-1B"  # Choose "Llama-2-13b-hf" if you have more resources
# quantization_config = BitsAndBytesConfig(load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", quantization_config=quantization_config)
# Load the model with `torch.float16` precision
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map={"": "mps"}  # Use MPS (Apple Metal) if available
)
# Create a summarization pipeline using the model
summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=150)

# Load the original JSON with detailed descriptions
with open("entity_descriptions.json", "r") as file:
    entity_descriptions = json.load(file)

# Function to summarize each description with strict instructions to avoid adding information
def summarize_strictly(description):
    prompt = f"""
    Summarize the {description} in a short and concise way.
    """
    
    
    # Generate a summary with strict word count control
    summary = summarizer(prompt, max_length=150, num_return_sequences=1, do_sample=False)[0]['generated_text']
    
    # Post-process to remove the prompt part if it’s included in the output
    return summary.split("\n\n")[1].strip() if "\n\n" in summary else summary.strip()

# Create a new dictionary for the summarized results
entity_summaries = {entity: summarize_strictly(description) for entity, description in entity_descriptions.items()}

# Save the summarized descriptions to a new JSON file
with open("entity_summarized.json", "w") as file:
    json.dump(entity_summaries, file, indent=4)

print("Summarized entity descriptions saved to entity_summarized.json")
