import os
import re
import json
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
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
    result = [sentence_entities[0]]
    for entity in sentence_entities[1:]:
        word, end, score = entity["word"], entity["end"], entity["score"]
        last_pick = result[-1]
        if entity["start"] - last_pick["end"] <= 1:
            last_pick["word"] += word[2] if word.startswith("##") else (" " + word)
            last_pick["end"] = end
            last_pick["score"] = score
        else:
            result.append(entity.copy())
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

# Initialize additional models
llm = ClientFactory.createModel(model="mistral")
llm = ClientFactory.createModel(model="internlm_25")
embedder = ClientFactory.createModel(model="mobal")

assessor = """
Given this response to a question, can you say if this response is closer to a 'yes' or a 'no'?
Question: {question}
Response: {response}
"""

# Output parsing function
def output_parser(text):
    iterator = map(lambda x: re.sub(r"\W+", "", x), text.replace("</s>", "").lower().split())
    try:
        return next(filter(lambda _ : _ in ["no", "yes", "missing"], iterator))
    except Exception as e:
        print("exception:", e)

# Function to refine summary for each entity
def map_refine_summary(entity, chunks):
    question = f"Provide a very concise and short description about {entity} based on the article."
    query = mapRefineQuery(map_prompt, refine_prompt, llm, refined_input_name="article")
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
    ner_results = nlp(new_document)
    aggregated_result = [aggregate_ner_results(ner_sentence) for ner_sentence in ner_results]
    
    # Filter and clean results
    cleaned_aggregated_result = [
        entity for sentence_entities in aggregated_result for entity in sentence_entities
        if entity and any(_ in entity["entity"] for _ in ["ORG", "LOC", "PER"])
    ]
    cleaned_aggregated_result = list(map(lambda x: x["word"].lower().strip(), cleaned_aggregated_result))
    
    # Summarize each entity
    dict_entity_summaries = {}
    for entity in tqdm(cleaned_aggregated_result):
        dict_entity_summaries[entity] = map_refine_summary(entity, process_articles_summarization(input_path))
    
    # Save results to JSON
    with open(output_path + "dict_entity_summaries.json", "w") as outfile:
        json.dump(dict_entity_summaries, outfile)
