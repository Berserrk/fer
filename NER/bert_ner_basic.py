import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from docx import Document
from typing import List, Dict
import json
import os
from datetime import datetime

class BertNERProcessor:
    def __init__(self, model_name="dbmdz/bert-large-cased-finetuned-conll03-english"):
        """Initialize tokenizer and model for NER processing."""
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.label_list = ["O", "B-MISC", "I-MISC", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]

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
        for i, pred in enumerate(predictions[0]):
            label_id = pred.item()
            label = self.label_list[label_id]
            if label != "O":  # Ignore non-entity tokens
                entities.append({
                    "word": self.tokenizer.convert_ids_to_tokens(tokens["input_ids"][0][i].item()),
                    "entity": label
                })
        return entities

    def group_entities(self, entities: List[Dict[str, str]]) -> Dict[str, List[str]]:
        """Group recognized entities by type."""
        grouped_entities = {"MISC": [], "PER": [], "ORG": [], "LOC": []}
        for entity in entities:
            label = entity["entity"][2:]  # Strip B- or I- prefix
            word = entity["word"]
            if label in grouped_entities:
                grouped_entities[label].append(word)
        return grouped_entities

    def save_entities_to_json(self, entities: Dict[str, List[str]], output_path: str) -> str:
        """Save the recognized entities to a JSON file."""
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

    # Group entities by type
    grouped_entities = processor.group_entities(entities)
    print("Grouped entities by type.")

    # Save results to JSON
    output_file = processor.save_entities_to_json(grouped_entities, output_path)
    print(f"Entities saved to: {output_file}")

if __name__ == "__main__":
    input_path = "inputs/breaking_news.docx"
    output_path = "outputs/output_entities.json"
    main(input_path, output_path)
