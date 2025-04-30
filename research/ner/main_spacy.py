import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Your input text
text = """
Mister Louis Aragorn is a business man that is involved in money laudering.
His son Frodo aragorn is an artist involved in fraud.
His wife Arwen is involved in sports.
Frodon told Aragorn that he likes to play football.
Arwen loves to travel.
Jean is present but not Meritservus.
Frodo is absent today.
Lord frodon might be here.
"""

# Process the text with the NER pipeline
doc = nlp(text)

# Extract entities
entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["PERSON", "ORG"]]
print(entities)
