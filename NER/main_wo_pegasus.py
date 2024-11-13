import spacy
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
import json
from transformers import pipeline

# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load Sentence-BERT model for embeddings
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Example text input
text = """
The president of the united states Barack Obama has started to travel in ASIA.
Obama is still trying to prevent a war in Taiwan.
Barack as his wife call him, is really appreciated in Japan by the population
"""


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

## Summarize

# Load the summarization model (e.g., PEGASUS)
summarizer = pipeline("summarization", model="google/pegasus-xsum")

# Load the original JSON with detailed descriptions
with open("entity_descriptions.json", "r") as file:
    entity_descriptions = json.load(file)

import json
from transformers import pipeline

# Load the summarization model (PEGASUS, T5, etc.)
summarizer = pipeline("summarization", model="google/pegasus-xsum")

# Load the original JSON with detailed descriptions
with open("entity_descriptions.json", "r") as file:
    entity_descriptions = json.load(file)

# Function to summarize strictly using only the provided text
def summarize_strictly(description):
    # Formulate a prompt asking the model to summarize strictly based on the input text
    context = "You are an assistant that is summarizing shortly and concisely the text provided"
    prompt = f"""
    Summarize strictly the text provided in a more concise way and less than 30 words
    """
    
    # Perform the summarization with a strict word limit
    summarized = summarizer(prompt, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    
    return summarized

# Create summarized descriptions based on the strict rules
entity_summaries = {}
for entity, description in entity_descriptions.items():
    entity_summaries[entity] = summarize_strictly(description)

# Save the new summaries into a file
with open("entity_summarized.json", "w") as file:
    json.dump(entity_summaries, file, indent=4)
print("entity_summaries", entity_summaries)

print("Strict summaries based only on provided text saved to entity_summarized.json")
