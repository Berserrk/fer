import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import openai
import re
import json
from typing import List, Dict, Tuple

class LLMEntityMatcher:
    def __init__(self, api_key: str):
        """Initialize the matcher with OpenAI API key"""
        openai.api_key = api_key
        
    def clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        if not isinstance(text, str):
            return str(text)
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return ' '.join(text.split())

    def calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calculate basic name similarity"""
        name1_clean = self.clean_text(name1)
        name2_clean = self.clean_text(name2)
        return SequenceMatcher(None, name1_clean, name2_clean).ratio()

    async def compare_descriptions(self, desc1: str, desc2: str) -> Dict:
        """Use LLM to directly compare two descriptions"""
        prompt = f"""Compare these two entity descriptions and analyze their similarity:

Description 1: {desc1}
Description 2: {desc2}

Provide a JSON response with:
1. A similarity score between 0 and 1
2. Key matching aspects
3. Key differences
4. Confidence in the comparison

Format:
{{
    "similarity_score": float,
    "matching_aspects": [str],
    "differences": [str],
    "confidence": float
}}"""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in entity resolution and semantic analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error in LLM comparison: {e}")
            return {
                "similarity_score": 0.0,
                "matching_aspects": [],
                "differences": ["Error in comparison"],
                "confidence": 0.0
            }

    async def find_matches(
        self,
        df: pd.DataFrame,
        name_threshold: float = 0.7,
        desc_threshold: float = 0.7,
        name_weight: float = 0.3
    ) -> List[Dict]:
        """Find matching entities using LLM comparison"""
        matches = []
        
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                record1 = df.iloc[i]
                record2 = df.iloc[j]
                
                # First check name similarity to filter obvious non-matches
                name_sim = self.calculate_name_similarity(record1['name'], record2['name'])
                
                if name_sim >= name_threshold:
                    # Get LLM comparison for descriptions
                    llm_result = await self.compare_descriptions(
                        record1['description'],
                        record2['description']
                    )
                    
                    desc_sim = llm_result['similarity_score']
                    
                    # Calculate weighted similarity
                    weighted_sim = (name_sim * name_weight + 
                                  desc_sim * (1 - name_weight))
                    
                    if desc_sim >= desc_threshold:
                        match = {
                            'record1_id': record1.name,
                            'record2_id': record2.name,
                            'record1_name': record1['name'],
                            'record2_name': record2['name'],
                            'overall_similarity': weighted_sim,
                            'name_similarity': name_sim,
                            'description_similarity': desc_sim,
                            'matching_aspects': llm_result['matching_aspects'],
                            'differences': llm_result['differences'],
                            'confidence': llm_result['confidence']
                        }
                        matches.append(match)
        
        return matches

# Example usage:
"""
# Initialize matcher
matcher = LLMEntityMatcher(api_key='your-api-key')

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

df = pd.DataFrame(data)

# Find matches
matches = await matcher.find_matches(
    df,
    name_threshold=0.7,
    desc_threshold=0.7,
    name_weight=0.3
)

# Display results
for match in matches:
    print(f"\nMatch Found (Overall Similarity: {match['overall_similarity']:.2f}):")
    print(f"Record 1: {match['record1_name']}")
    print(f"Record 2: {match['record2_name']}")
    print("\nMatching Aspects:")
    for aspect in match['matching_aspects']:
        print(f"- {aspect}")
    print("\nKey Differences:")
    for diff in match['differences']:
        print(f"- {diff}")
    print(f"Confidence: {match['confidence']:.2f}")
"""
