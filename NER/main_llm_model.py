import spacy
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from promp_text import text
# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load Sentence-BERT model for embeddings
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Example text input



# Step 1: Extract Entities from Text
doc = nlp(text)
entities = []
for ent in doc.ents:
    if ent.label_ in ["PERSON", "ORG", "GPE"]:
        entities.append(ent.text)

# Remove duplicate entities
entities = list(set(entities))
print("entities:", entities)

# Step 2: Create Embeddings and Cluster Entities
embeddings = sbert_model.encode(entities)
clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.0)
clusters = clustering_model.fit_predict(embeddings)

# Group entities by cluster labels
clustered_entities = {}
for i, label in enumerate(clusters):
    clustered_entities.setdefault(label, []).append(entities[i])

print("clustered_entities:", clustered_entities)

# Step 3: Extract and Combine Context for Each Cluster
entity_descriptions = {}
for label, entity_group in clustered_entities.items():
    context_sentences = []
    for entity in entity_group:
        for sent in doc.sents:
            if entity in sent.text:
                context_sentences.append(sent.text)
    description = " ".join(context_sentences)
    entity_descriptions[entity_group[0]] = description

# Step 4: Save to JSON
with open("entity_descriptions.json", "w") as file:
    json.dump(entity_descriptions, file, indent=4)

# Summarization with Strict Constraints

model_name = "meta-llama/Llama-2-7b-hf"  # Replace with a more reliable model for summarization if available
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load model on MPS if available
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

summarizer = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0,  # Change to -1 for CPU-only
)

# Function to summarize each description with constrained generation
def summarize_strictly(description):
    prompt = f"Summarize the following description without adding extra information:\n\n{description}\n\n"
    summary = summarizer(
        prompt,
        max_length=100,
        do_sample=False,
        temperature=0.3,  # Lower temperature to reduce randomization
        top_p=0.9,
        top_k=50,
        num_return_sequences=1,
    )[0]['generated_text']
    
    # Remove prompt from the output if needed
    return summary.replace(prompt, "").strip()

# Summarize each entity description
entity_summaries = {entity: summarize_strictly(description) for entity, description in entity_descriptions.items()}

# Save summarized descriptions to JSON
with open("entity_summarized.json", "w") as file:
    json.dump(entity_summaries, file, indent=4)

print("Summarized entity descriptions saved to entity_summarized.json")
