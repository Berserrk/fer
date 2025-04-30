import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from docx import Document
from typing import List, Dict
import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np

class BertNERProcessor:
    def __init__(self, model_name="dbmdz/bert-large-cased-finetuned-conll03-english"):
        """Initialize tokenizer, NER model, and sentence embedding model."""
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.label_list = ["O", "B-MISC", "I-MISC", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # For similarity clustering

    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file."""
        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    def perform_ner(self, text: str) -> List[Dict[str, str]]:
        """Perform Named Entity Recognition on the input text."""
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**tokens).logits
        predictions = torch.argmax(outputs, dim=2)

        entities = []
        current_entity = []
        current_label = None
        for i, pred in enumerate(predictions[0]):
            label_id = pred.item()
            label = self.label_list[label_id]
            if label != "O":
                entity_type = label[2:]  # Get the entity type (e.g., PER, LOC)
                word = self.tokenizer.convert_ids_to_tokens(tokens["input_ids"][0][i].item())
                if current_label == label:
                    current_entity.append(word)
                else:
                    if current_entity:
                        entities.append({"entity": " ".join(current_entity), "type": current_label[2:]})
                    current_entity = [word]
                    current_label = label
            elif current_entity:
                entities.append({"entity": " ".join(current_entity), "type": current_label[2:]})
                current_entity = []
                current_label = None
        return entities

    def cluster_entities(self, entities: List[Dict[str, str]]) -> Dict[str, List[Dict[str, List[str]]]]:
        """Cluster similar entities using embeddings and DBSCAN."""
        grouped_entities = {"MISC": [], "PER": [], "ORG": [], "LOC": []}
        for entity_type in grouped_entities.keys():
            type_entities = [e["entity"] for e in entities if e["type"] == entity_type]

            # Create embeddings
            embeddings = self.embedding_model.encode(type_entities)
            clustering = DBSCAN(eps=0.5, min_samples=1, metric="cosine").fit(embeddings)

            # Group entities by cluster labels
            clusters = {}
            for idx, label in enumerate(clustering.labels_):
                entity = type_entities[idx]
                if label not in clusters:
                    clusters[label] = {"main": entity, "variations": []}
                else:
                    clusters[label]["variations"].append(entity)

            # Add clusters to grouped entities
            grouped_entities[entity_type] = list(clusters.values())
        return grouped_entities

    def save_entities_to_json(self, entities: Dict[str, List[Dict[str, List[str]]]], output_path: str) -> str:
        """Save the recognized and clustered entities to a JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        json_output = {
            "metadata": {
                "processing_date": datetime.now().isoformat(),
            },
            "entities": entities
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=4)
        return output_path

def main(input_path: str, output_path: str):
    processor = BertNERProcessor()
    
    # Extract text from DOCX
    text = processor.extract_text_from_docx(input_path)
    print("Extracted text from DOCX.")

    # Perform Named Entity Recognition
    entities = processor.perform_ner(text)
    print("Performed NER on the text.")

    # Cluster similar entities
    clustered_entities = processor.cluster_entities(entities)
    print("Clustered similar entities.")

    # Save results to JSON
    output_file = processor.save_entities_to_json(clustered_entities, output_path)
    print(f"Entities saved to: {output_file}")

if __name__ == "__main__":
    input_path = "inputs/breaking_news.docx"
    output_path = "outputs/output_entities.json"
    main(input_path, output_path)
