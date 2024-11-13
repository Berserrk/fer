import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

class BertNERProcessor:
    def __init__(self):
        """Initialize models and NLP tools"""
        print("Loading models...")
        # BERT NER model
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.label_list = ["O", "B-MISC", "I-MISC", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
        
        # Sentence transformer for semantic similarity
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Models loaded successfully")

    def _extract_entities(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract named entities from text chunk"""
        print(f"\nProcessing text chunk: {text[:100]}...")
        
        # Tokenize input
        encoded = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**encoded)
        
        # Get predicted labels
        predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()
        
        # Get tokens
        token_ids = encoded["input_ids"][0].tolist()
        tokens = self.tokenizer.convert_ids_to_tokens(token_ids)
        
        # Initialize results
        entities = {
            'PERSON': [],
            'ORGANIZATION': [],
            'LOCATION': [],
            'MISCELLANEOUS': []
        }
        
        # Track current entity
        current_entity = []
        current_type = None
        
        # Process tokens and their predictions
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

        # Don't forget last entity
        if current_entity:
            self._add_complete_entity(entities, current_entity, current_type)

        print("\nExtracted entities:")
        print(json.dumps(entities, indent=2))
        
        return entities

    def _add_complete_entity(self, entities: Dict[str, List[Dict[str, str]]], 
                             token_list: List[str], entity_type: str) -> None:
        """Add a complete entity to the appropriate category"""
        if not token_list or not entity_type:
            return
            
        # Join tokens and clean up
        entity_text = ' '.join(token_list).replace(' ##', '').strip()
        if not entity_text:
            return
            
        entity_dict = {'text': entity_text, 'type': entity_type}
        
        # Map to correct category
        if entity_type == 'PER':
            entities['PERSON'].append(entity_dict)
        elif entity_type == 'ORG':
            entities['ORGANIZATION'].append(entity_dict)
        elif entity_type == 'LOC':
            entities['LOCATION'].append(entity_dict)
        elif entity_type == 'MISC':
            entities['MISCELLANEOUS'].append(entity_dict)
        
        print(f"Added entity: {entity_text} of type {entity_type}")

    def _cluster_entities(self, entities: Dict[str, List[Dict[str, str]]]) -> Dict[str, List[Dict[str, List[str]]]]:
        """Cluster similar entities together."""
        clustered_entities = {category: [] for category in entities}

        for category, items in entities.items():
            if not items:
                continue
            
            # Prepare a list of entity names for embedding
            entity_texts = [item['text'] for item in items]
            
            # Compute embeddings for the entity texts
            embeddings = self.semantic_model.encode(entity_texts)

            # Clustering using DBSCAN
            clustering_model = DBSCAN(eps=0.5, min_samples=1, metric='cosine')
            clustering_labels = clustering_model.fit_predict(embeddings)

            # Organize clustered entities
            clusters = {}
            for label, entity in zip(clustering_labels, entity_texts):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(entity)

            # Create the output structure
            for variations in clusters.values():
                main_text = variations[0]  # Choose the first as the main entity
                clustered_entities[category].append({
                    'main': main_text,
                    'variations': variations[1:]  # Exclude the main from variations
                })

        return clustered_entities

def write_results_to_file(results: Dict[str, List[Dict[str, List[str]]]], output_file: str) -> None:
    """Write clustered entities to a JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

def main():
    # Sample text for testing
    sample_text = """
    President of Russia, Vladimir Putin, announced new policies today. 
    Meanwhile, Joe Biden discussed matters with Dr. Smith and John Smith.
    Hillary Clinton was also present.
    """
    
    # Process the document
    processor = BertNERProcessor()
    extracted_entities = processor._extract_entities(sample_text)
    clustered_results = processor._cluster_entities(extracted_entities)
    
    # Write clustered results to a JSON file
    output_file = "named_entities_clustered_results.json"
    write_results_to_file(clustered_results, output_file)

if __name__ == "__main__":
    main()
