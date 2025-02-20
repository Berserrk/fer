# Import required libraries 
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

class EntityMatcher:
    def __init__(self, embedding_model='all-MiniLM-L6-v2'):
        """
        Initialize the entity matcher with specified embedding model
        
        Args:
            embedding_model: Model name for sentence-transformers or 'openai' for OpenAI embeddings
        """
        self.embedding_model = embedding_model
        if embedding_model != 'openai':
            # Load local sentence-transformers model
            self.model = SentenceTransformer(embedding_model)
    
    def clean_text(self, text):
        """Clean text by removing special characters and standardizing format"""
        if not isinstance(text, str):
            return str(text)
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        return text

    def calculate_name_similarity(self, name1, name2):
        """Calculate similarity between names using SequenceMatcher"""
        name1_clean = self.clean_text(name1)
        name2_clean = self.clean_text(name2)
        return SequenceMatcher(None, name1_clean, name2_clean).ratio()

    async def get_openai_embedding(self, text):
        """Get embeddings using OpenAI's API"""
        try:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error getting OpenAI embedding: {e}")
            return None

    def get_local_embedding(self, text):
        """Get embeddings using sentence-transformers"""
        try:
            embedding = self.model.encode(text, convert_to_tensor=True)
            return embedding
        except Exception as e:
            print(f"Error getting local embedding: {e}")
            return None

    def calculate_description_similarity(self, desc1, desc2):
        """Calculate similarity between descriptions using embeddings"""
        # Clean descriptions
        desc1_clean = self.clean_text(desc1)
        desc2_clean = self.clean_text(desc2)
        
        # Get embeddings
        if self.embedding_model == 'openai':
            # Use OpenAI embeddings (requires async)
            emb1 = await self.get_openai_embedding(desc1_clean)
            emb2 = await self.get_openai_embedding(desc2_clean)
        else:
            # Use local model embeddings
            emb1 = self.get_local_embedding(desc1_clean)
            emb2 = self.get_local_embedding(desc2_clean)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # Calculate cosine similarity
        if isinstance(emb1, torch.Tensor):
            emb1 = emb1.cpu().numpy()
            emb2 = emb2.cpu().numpy()
        
        similarity = cosine_similarity(
            emb1.reshape(1, -1),
            emb2.reshape(1, -1)
        )[0][0]
        
        return float(similarity)

    def find_matches(self, df, name_threshold=0.8, desc_threshold=0.7, name_weight=0.4):
        """Find matching entities based on name and description similarity"""
        matches = []
        total_comparisons = len(df) * (len(df) - 1) // 2
        
        print(f"Processing {total_comparisons} comparisons...")
        
        # Get all description embeddings first for efficiency
        descriptions = df['description'].apply(self.clean_text).tolist()
        if self.embedding_model != 'openai':
            all_embeddings = self.model.encode(descriptions, convert_to_tensor=True)
        
        # Compare all pairs
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                record1 = df.iloc[i]
                record2 = df.iloc[j]
                
                # Calculate name similarity
                name_sim = self.calculate_name_similarity(record1['name'], record2['name'])
                
                # Only proceed if names are similar enough
                if name_sim >= name_threshold:
                    # Calculate description similarity using cached embeddings
                    if self.embedding_model != 'openai':
                        desc_sim = float(cosine_similarity(
                            all_embeddings[i].reshape(1, -1),
                            all_embeddings[j].reshape(1, -1)
                        )[0][0])
                    else:
                        desc_sim = self.calculate_description_similarity(
                            record1['description'],
                            record2['description']
                        )
                    
                    # Calculate weighted similarity
                    weighted_sim = (name_sim * name_weight + 
                                  desc_sim * (1 - name_weight))
                    
                    # Check if description similarity meets threshold
                    if desc_sim >= desc_threshold:
                        match = {
                            'Record 1': f"ID: {record1.name}, Name: {record1['name']}",
                            'Record 2': f"ID: {record2.name}, Name: {record2['name']}",
                            'Overall Similarity': f"{weighted_sim:.2f}",
                            'Similarities': {
                                'name': f"{name_sim:.2f}",
                                'description': f"{desc_sim:.2f}"
                            },
                            'Description 1': record1['description'],
                            'Description 2': record2['description']
                        }
                        matches.append(match)
        
        return matches

# Example usage
def main():
    # Sample data
    data = {
        'name': [
            'John Smith',
            'Jon Smith',
            'Jane Doe',
            'J. Smith'
        ],
        'description': [
            'A software engineer with 10 years of experience in Python and Java development',
            'Experienced software developer specializing in Python and Java programming',
            'Marketing professional with expertise in digital campaigns',
            'Senior software engineer with Python and Java background'
        ]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)
    print("Input Data:")
    print(df)
    print("\n" + "="*80 + "\n")

    # Initialize matcher with chosen model
    matcher = EntityMatcher(embedding_model='all-MiniLM-L6-v2')  # or 'openai' for OpenAI embeddings
    
    # Find matches
    matches = matcher.find_matches(
        df,
        name_threshold=0.7,
        desc_threshold=0.7,
        name_weight=0.4  # Give more weight to description similarity
    )

    # Display results
    print("Matching Results:")
    for match in matches:
        print("\nMatch Found:")
        print(f"Record 1: {match['Record 1']}")
        print(f"Record 2: {match['Record 2']}")
        print(f"Overall Similarity: {match['Overall Similarity']}")
        print("Field-by-field similarities:")
        for field, sim in match['Similarities'].items():
            print(f"  {field}: {sim}")

if __name__ == "__main__":
    main()
