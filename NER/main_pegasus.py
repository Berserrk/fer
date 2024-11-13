import spacy
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from sklearn.cluster import AgglomerativeClustering
import json

# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load Sentence-BERT model for embeddings
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the summarization model from Hugging Face
summarizer = pipeline("summarization", model="google/pegasus-xsum")

# Example text input
text = """
In the fantasy world of Middle-earth, the Dark Lord Sauron created the One Ring to dominate all other magical rings of power and enslave their wearers. After losing the Ring in battle and being defeated, it passed through history until finding its way to a hobbit named Bilbo Baggins.
Years later, the wizard Gandalf discovers that Bilbo's ring is actually the One Ring. Bilbo's nephew Frodo inherits it, and Gandalf reveals that Sauron has risen again and seeks the Ring to restore his full power. Frodo must leave his peaceful home in the Shire and journey to the Elven refuge of Rivendell.
At Rivendell, a council determines the Ring must be destroyed by casting it into Mount Doom in Mordor - Sauron's realm - where it was forged. Frodo volunteers to undertake this perilous mission. Eight companions join him, forming the Fellowship of the Ring: his hobbit friends Sam, Merry, and Pippin; the wizard Gandalf; the humans Aragorn and Boromir; the elf Legolas; and the dwarf Gimli.
The Fellowship faces many dangers but ultimately breaks apart. Boromir tries to take the Ring, falls to its corruption, and dies defending Merry and Pippin from orcs. Frodo and Sam continue alone toward Mordor, while the others pursue the orcs who captured their hobbit friends.
Frodo and Sam are joined by Gollum, a corrupted creature who once possessed the Ring. He guides them to Mordor but ultimately betrays them. Meanwhile, Gandalf returns from death more powerful, and helps rally the kingdoms of men against Sauron's forces.
The other members of the Fellowship aid in defending the kingdom of Rohan from Saruman (a corrupted wizard) and help Gondor resist Sauron's armies. Aragorn claims his heritage as heir to Gondor's throne and rallies more forces to the cause.
As massive battles rage, Frodo, Sam, and Gollum reach Mount Doom. At the crucial moment, Frodo succumbs to the Ring's power and claims it for himself. However, Gollum attacks him and takes the Ring, but falls into the volcano with it, destroying both himself and the Ring.
Sauron is permanently destroyed, and Middle-earth is saved. The hobbits return home as heroes, though changed by their experiences. Aragorn becomes King of the reunited kingdoms of men, and marries the elf Arwen. Most of the elves, including Gandalf, depart Middle-earth for the Undying Lands across the sea. Years later, Frodo, still wounded by his quest, joins them, leaving Sam to live a full life in the Shire.
The story explores themes of good versus evil, the corrupting nature of power, the strength found in friendship and loyalty, and how even the smallest person can change the world's fate. It shows that victory often requires sacrifice and that some wounds never fully heal, but hope and goodness can triumph over darkness.
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

### Step 3: Generate Summaries for Each Cluster
# We’ll use the summarizer to provide descriptions for each group
entity_summaries = {}
for label, entity_group in clustered_entities.items():
    # Join entities into a single string for context
    entity_text = "; ".join(entity_group)
    # Generate a summary (description) of the entity group
    summary = summarizer(entity_text, max_length=60, min_length=25, do_sample=False)[0]['summary_text']
    # Use the main entity as the key in JSON output, with the summary as the value
    entity_summaries[entity_group[0]] = summary

### Step 4: Export to JSON Format
json_output = json.dumps(entity_summaries, indent=4)
print(json_output)

# Optionally save to a file
with open("entity_summaries.json", "w") as file:
    file.write(json_output)
