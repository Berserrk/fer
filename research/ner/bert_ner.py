import re
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np
import json
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from typing import List, Dict, Set

class BertNERProcessor:
    def __init__(self):
        print("Loading models...")
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.label_list = ["O", "B-MISC", "I-MISC", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Models loaded successfully")

    def process_text(self, text: str) -> Dict[str, List[Dict[str, List[str]]]]:
        entities = self._extract_entities(text)
        grouped_entities = self._group_entities(entities)
        return grouped_entities

    def _group_entities(self, entities: Dict[str, List[Dict[str, str]]]) -> Dict[str, List[Dict[str, List[str]]]]:
        """Cluster and group similar entities with variations."""
        grouped_results = {}
        
        for category, entity_list in entities.items():
            if not entity_list:
                continue

            entity_texts = [entity['text'] for entity in entity_list]
            embeddings = self.semantic_model.encode(entity_texts)

            clustering_model = DBSCAN(eps=0.3, min_samples=1, metric='cosine')
            cluster_labels = clustering_model.fit_predict(embeddings)
            
            clusters = {}
            for label, entity_text in zip(cluster_labels, entity_texts):
                if label not in clusters:
                    clusters[label] = {'main': entity_text, 'variations': set()}
                clusters[label]['variations'].add(entity_text)
            
            # Set the `main` entity as the most complete version or first in the cluster
            grouped_results[category] = [
                {'main': self._select_main_entity(cluster['variations']),
                 'variations': list(cluster['variations'] - {self._select_main_entity(cluster['variations'])})}
                for cluster in clusters.values()
            ]
        
        return grouped_results

    def _select_main_entity(self, variations: Set[str]) -> str:
        """Choose the most informative name from variations, favoring full names and avoiding titles only."""
        return sorted(variations, key=lambda name: (-len(name), name))[0]

    def _extract_entities(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract entities while handling titles like 'Mr.', 'Dr.', etc., and subword tokens."""
        honorifics = {"Mr.", "Mrs.", "Dr.", "Ms.", "Miss", "President"}
        
        encoded = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**encoded)
        
        predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()
        token_ids = encoded["input_ids"][0].tolist()
        tokens = self.tokenizer.convert_ids_to_tokens(token_ids)
        
        entities = {
            'PERSON': [],
            'ORGANIZATION': [],
            'LOCATION': [],
            'MISCELLANEOUS': []
        }
        
        current_entity = []
        current_type = None

        for token, pred_idx in zip(tokens, predictions):
            pred_label = self.label_list[pred_idx]

            # Skip special tokens
            if token in ['[CLS]', '[SEP]', '[PAD]']:
                continue

            # Handle subword tokens that begin with "##"
            if token.startswith("##") and current_entity:
                token = token[2:]  # Remove '##' prefix
                current_entity[-1] += token  # Append subword to the previous token
            elif pred_label.startswith('B-') or (pred_label.startswith('I-') and not current_entity):
                if current_entity:
                    self._add_complete_entity(entities, current_entity, current_type)
                current_entity = [token]
                current_type = pred_label[2:]
            
            elif pred_label.startswith('I-') and current_entity:
                current_entity.append(token)
            
            elif pred_label == 'O' and current_entity:
                self._add_complete_entity(entities, current_entity, current_type)
                current_entity = []
                current_type = None

        if current_entity:
            self._add_complete_entity(entities, current_entity, current_type)
        
        return entities


    def _add_complete_entity(self, entities: Dict[str, List[Dict[str, str]]], token_list: List[str], entity_type: str):
        """Add an entity to the appropriate category with honorific handling."""
        if not token_list or not entity_type:
            return
        
        entity_text = ' '.join(token_list).strip()
        
        # Check if the first word is an honorific and include it in the entity text
        if token_list[0] in {"Mr", "Mrs", "Dr", "Ms", "Miss", "President"}:
            entity_text = token_list[0] + ' ' + ' '.join(token_list[1:]).strip()
        
        entity_dict = {'text': entity_text, 'type': entity_type}
        
        # Assign to correct category
        if entity_type == 'PER':
            entities['PERSON'].append(entity_dict)
        elif entity_type == 'ORG':
            entities['ORGANIZATION'].append(entity_dict)
        elif entity_type == 'LOC':
            entities['LOCATION'].append(entity_dict)
        elif entity_type == 'MISC':
            entities['MISCELLANEOUS'].append(entity_dict)

def main():
    sample_text = """
    Mr. Putin announced new policies today. Vladimir Putin has been in power for many years.
    Putin spoke about various issues. Meanwhile, Joe Biden and President Biden discussed matters
    with Dr. Smith and John Smith. The meeting was also attended by Mrs. Clinton and Hillary Clinton.
    """
    
    processor = BertNERProcessor()
    results = processor.process_text(sample_text)
    
    output_file = "named_entities_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
