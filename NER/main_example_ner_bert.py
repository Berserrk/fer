import os
import re
import json
from tqdm import tqdm
from llama_index import LLMPredictor, GPT3LLMPredictor, PromptHelper
from some_module import Document, RecursiveCharacterTextSplitter, mapRefineQuery

# Load spaCy NER model
import spacy
nlp = spacy.load("en_core_web_sm")

# Define constants for chunking and splitting
SPLITTER_KWARGS = {
    "chunk_size": 1000,
    "chunk_overlap": 500,
    "separators": ["\n\n", "\n", ".", ";", ":", "?", "!", ",", " "],
    "is_separator_regex": False,
}

# Function to process articles
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
                "score": 1.0  # spaCy doesn't provide a score, so we set it to 1.0
            })
    return result

# Define prompt for refining summaries
map_prompt = """Context information is below.
---------------------
{article}
Given the context information and no prior knowledge, answer concisely the question: {question}"""

refine_prompt = """The original question is as follows: {question}
We have provided an existing answer: {response}
Please refine the existing answer (if needed) with more context below.
---------------------
{article}"""

# Summarization chunking
CHUNK_LENGTH = 10000
SPLITTER_SUMMARIZATION_KWARGS = {
    "chunk_size": CHUNK_LENGTH,
    "chunk_overlap": 1000,
    "separators": ["\n\n", "\n", ".", ";", ":", "?", "!", ",", " "],
    "is_separator_regex": False,
    "length_function": len
}

def process_articles_summarization(input_path):
    doc_article = Document(input_path)
    splitter = RecursiveCharacterTextSplitter(**SPLITTER_SUMMARIZATION_KWARGS)
    chunks = splitter.create_documents(texts=list(map(lambda x: x.text, doc_article.paragraphs)))
    chunks = splitter.split_documents(chunks)
    new_chunks = [chunks[0]]
    for _ in chunks[1:]:
        if (len(new_chunks[-1]) + len(_)) < CHUNK_LENGTH:
            new_chunks[-1] += _
        else:
            new_chunks.append(_)
    return new_chunks

# Initialize Llama-3.2-1B model
llm_predictor = GPT3LLMPredictor(model_path="path/to/llama-3.2-1B")
prompt_helper = PromptHelper(max_input_size=4096, num_output=2048, max_chunk_overlap=20)

# Function to refine summary for each entity
def map_refine_summary(entity, chunks):
    question = f"Provide a very concise and short description about {entity} based on the article."
    query = mapRefineQuery(map_prompt, refine_prompt, llm_predictor, prompt_helper, refined_input_name="article")
    return query.invoke({"question": question, "article": chunks})

# Directory setup and listing articles
name_articles = os.listdir("inputs/")
name_articles = [s.replace('.docx', '') for s in name_articles]
print(name_articles)

# Loop through articles to get summaries and save them
for article in name_articles:
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
    dict_entity_summaries = {}
    for entity in tqdm(cleaned_aggregated_result):
        dict_entity_summaries[entity] = map_refine_summary(entity, process_articles_summarization(input_path))
    
    # Save results to JSON
    with open(output_path + "dict_entity_summaries.json", "w") as outfile:
        json.dump(dict_entity_summaries, outfile)