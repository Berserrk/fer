import os
import re
import json
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from llama_index import LLMPredictor, GPT3LLMPredictor, PromptHelper
from some_module import Document, RecursiveCharacterTextSplitter, mapRefineQuery

# Load tokenizer and model for NER
MAX_NER_LENGTH = 1000
tokenizer = AutoTokenizer.from_pretrained("/domino/datasets/local/article_detective/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("/domino/datasets/local/article_detective/bert-large-NER").cuda()
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Define constants for chunking and splitting
SPLITTER_KWARGS = {
    "chunk_size": MAX_NER_LENGTH,
    "chunk_overlap": 500,
    "separators": ["\n\n", "\n", ".", ";", ":", "?", "!", ",", " "],
    "is_separator_regex": False,
}

# Function to process articles
def process_articles(input_path):
    doc_article = Document(input_path)
    splitter = RecursiveCharacterTextSplitter(tokenizer=tokenizer, **SPLITTER_KWARGS)
    return [split for split in map(lambda x: splitter.split_text(x.text), doc_article.paragraphs)]

# Preprocess text function
def preprocess_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Aggregate NER results
def aggregate_ner_results(sentence_entities):
    # (Same as previous code)

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
    # (Same as previous code)

# Initialize Llama-3.2-1B model
llm_predictor = GPT3LLMPredictor(model_path="path/to/llama-3.2-1B")
prompt_helper = PromptHelper(max_input_size=4096, num_output=2048, max_chunk_overlap=20)

# Function to refine summary for each entity
def map_refine_summary(entity, chunks):
    question = f"Provide a very concise and short description about {entity} based on the article."
    query = mapRefineQuery(map_prompt, refine_prompt, llm_predictor, prompt_helper, refined_input_name="article")
    return query.invoke({"question": question, "article": chunks})

# Directory setup and listing articles
# (Same as previous code)

# Loop through articles to get summaries and save them
for article in name_articles:
    input_path = "inputs/" + article + ".docx"
    output_path = "outputs/" + article + "/"
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    new_document = list(map(preprocess_text, process_articles(input_path)))
    ner_results = nlp(new_document)
    aggregated_result = [aggregate_ner_results(ner_sentence) for ner_sentence in ner_results]
    
    # Filter and clean results
    # (Same as previous code)
    
    # Summarize each entity
    dict_entity_summaries = {}
    for entity in tqdm(cleaned_aggregated_result):
        dict_entity_summaries[entity] = map_refine_summary(entity, process_articles_summarization(input_path))
    
    # Save results to JSON
    with open(output_path + "dict_entity_summaries.json", "w") as outfile:
        json.dump(dict_entity_summaries, outfile)