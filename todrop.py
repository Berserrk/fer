# with name and entity description

# Import required libraries 
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    """Clean text by removing special characters and standardizing format"""
    if not isinstance(text, str):
        return str(text)
    
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def calculate_name_similarity(name1, name2):
    """Calculate similarity between names using SequenceMatcher"""
    name1_clean = clean_text(name1)
    name2_clean = clean_text(name2)
    return SequenceMatcher(None, name1_clean, name2_clean).ratio()

def calculate_description_similarity(desc1, desc2):
    """Calculate similarity between descriptions using TF-IDF and cosine similarity"""
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        token_pattern=r'\b\w+\b',  # Match whole words only
        min_df=1  # Include all terms since we're only comparing two documents
    )
    
    # Fit and transform the descriptions
    try:
        tfidf_matrix = vectorizer.fit_transform([clean_text(desc1), clean_text(desc2)])
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0

def find_matches(df, name_threshold=0.8, desc_threshold=0.3, name_weight=0.6):
    """Find matching entities based on name and description similarity
    
    Args:
        df: DataFrame with 'name' and 'description' columns
        name_threshold: Minimum similarity threshold for names
        desc_threshold: Minimum similarity threshold for descriptions
        name_weight: Weight given to name similarity (1 - name_weight for description)
    """
    matches = []
    
    # Compare all pairs
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            record1 = df.iloc[i]
            record2 = df.iloc[j]
            
            # Calculate name similarity
            name_sim = calculate_name_similarity(record1['name'], record2['name'])
            
            # Only proceed if names are similar enough
            if name_sim >= name_threshold:
                # Calculate description similarity
                desc_sim = calculate_description_similarity(
                    record1['description'], 
                    record2['description']
                )
                
                # Calculate weighted average similarity
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
                        }
                    }
                    matches.append(match)
    
    return matches

# Example usage with sample data
data = {
    'name': [
        'John Smith',
        'Jon Smith',2
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

# Find matches
matches = find_matches(df, name_threshold=0.7, desc_threshold=0.3, name_weight=0.6)

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
