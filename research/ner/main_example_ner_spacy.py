import os
import re
import json
from tqdm import tqdm
from collections import defaultdict
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import spacy
import openai

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Define constants for chunking and splitting
SPLITTER_KWARGS = {
    "chunk_size": 1000,
    "chunk_overlap": 500,
    "separators": ["\n\n", "\n", ".", ";", ":", "?", "!", ",", " "],
    "is_separator_regex": False,
}

# Function to process articles
@lru_cache(maxsize=1024)
def process_articles(input_path):
    doc_article = Document(input_path)
    splitter = RecursiveCharacterTextSplitter(**SPLITTER_KWARGS)
    return [split for split in map(lambda x: splitter.split_text(x.text), doc_article.paragraphs)]

# Preprocess text function
def preprocess_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Aggregate NER results
def aggregate_ner_results(ner_entities):
    result = []
    for entity in ner_entities:
        if entity.label_ in ["ORG", "LOC", "PER"]:
            result.append({
                "word": entity.text,
                "start": entity.start_char,
                "end": entity.end_char,
                "entity": entity.label_,
                "score": 1.0
            })
    return result

# Function to summarize text using OpenAI Whisper
def summarize_text(text, max_tokens=100):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following text in {max_tokens} tokens or less:\n\n{text}",
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Directory setup and listing articles
name_articles = os.listdir("inputs/")
name_articles = [s.replace('.docx', '') for s in name_articles]
print(name_articles)

# Load existing summaries
summary_cache = defaultdict(dict)
for article in name_articles:
    output_path = "outputs/" + article + "/"
    if os.path.exists(output_path + "dict_entity_summaries.json"):
        with open(output_path + "dict_entity_summaries.json", "r") as infile:
            summary_cache[article] = json.load(infile)

# Process articles in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    for article in name_articles:
        executor.submit(
            process_and_save_article,
            article,
            summary_cache[article]
        )

def process_and_save_article(article, existing_summaries):
    input_path = "inputs/" + article + ".docx"
    output_path = "outputs/" + article + "/"
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    new_document = list(map(preprocess_text, process_articles(input_path)))
    ner_results = [aggregate_ner_results(doc.ents) for doc in map(nlp, new_document)]
    aggregated_result = [entity for sentence_entities in ner_results for entity in sentence_entities]
    
    # Filter and clean results
    cleaned_aggregated_result = [
        entity for entity in aggregated_result
        if any(_ in entity["entity"] for _ in ["ORG", "LOC", "PER"])
    ]
    cleaned_aggregated_result = list(map(lambda x: x["word"].lower().strip(), cleaned_aggregated_result))
    
    # Summarize each entity
    dict_entity_summaries = existing_summaries.copy()
    for entity in tqdm(cleaned_aggregated_result):
        if entity not in dict_entity_summaries:
            dict_entity_summaries[entity] = summarize_text(
                " ".join(process_articles_summarization(input_path)), max_tokens=100
            )
    
    # Save results to JSON
    with open(output_path + "dict_entity_summaries.json", "w") as outfile:
        json.dump(dict_entity_summaries, outfile)

process_and_save_article("example_article", {})