common_industry_terms = {
    # Company types and legal entities
    'inc', 'ltd', 'llc', 'corp', 'corporation', 'company', 'co', 'group', 'holdings', 
    'enterprises', 'international', 'global', 'worldwide', 'national', 'incorporated',
    'limited', 'partners', 'partnership', 'gmbh', 'srl', 'sa', 'ag', 'bv', 'pte',
    
    # Industry descriptors
    'marine', 'services', 'shipping', 'logistics', 'transport', 'transportation', 
    'cargo', 'freight', 'forwarding', 'trading', 'trader', 'import', 'export',
    'commercial', 'business', 'industrial', 'industries', 'solutions', 'systems',
    
    # Maritime specific
    'shipping', 'maritime', 'sea', 'ocean', 'port', 'harbor', 'vessel', 'boat',
    'ship', 'tanker', 'carrier', 'fleet', 'navigation', 'offshore', 'voyages',
    
    # General business terms
    'association', 'agency', 'bureau', 'center', 'centre', 'office', 'department',
    'division', 'unit', 'management', 'consulting', 'consultancy', 'advisory',
    'resources', 'operations', 'ventures', 'investment', 'investments',
    
    # Geographical/regional indicators
    'middle', 'east', 'west', 'north', 'south', 'central', 'eastern', 'western',
    'northern', 'southern', 'regional', 'local', 'international', 'gulf', 'asia',
    'european', 'american', 'africa', 'pacific', 'atlantic',
    
    # Common words in company names
    'the', 'and', 'of', 'for', 'to', 'by', 'on', 'with', 'in', 'al', 'el'
}

import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import re

def clean_name(name):
    """Clean and standardize name format"""
    if not isinstance(name, str):
        return str(name)
    
    # Convert to lowercase
    name = name.lower()
    # Remove special characters
    name = re.sub(r'[^\w\s]', '', name)
    # Remove extra whitespace
    name = ' '.join(name.split())
    return name

def tokenize_name(name):
    """Split name into tokens"""
    return clean_name(name).split()

def jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity between two sets"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def sequence_similarity(s1, s2):
    """Calculate SequenceMatcher similarity"""
    return SequenceMatcher(None, s1, s2).ratio()

def subset_match(name1, name2):
    """Check if one name is a subset of another"""
    tokens1, tokens2 = tokenize_name(name1), tokenize_name(name2)
    return 1.0 if set(tokens1).issubset(set(tokens2)) or set(tokens2).issubset(set(tokens1)) else 0.0

def word_position_bonus(name1, name2):
    """Increase similarity score based on matching word positions with added weight for longer names"""
    tokens1, tokens2 = tokenize_name(name1), tokenize_name(name2)
    min_length = min(len(tokens1), len(tokens2))
    
    score = 0.0
    weight = 1.0  # Start weight, more for first words
    for i in range(min_length):
        if tokens1[i] == tokens2[i]:
            score += weight
        weight *= 0.8  # Decrease weight for each subsequent word match
    
    return min(score, 1.0)  # Cap the score at 1.0

def common_words_bonus(name1, name2):
    """Increase similarity score based on the number of common words"""
    tokens1, tokens2 = set(tokenize_name(name1)), set(tokenize_name(name2))
    common_tokens = tokens1.intersection(tokens2)
    
    return len(common_tokens) / max(len(tokens1), len(tokens2))

def calculate_name_similarity(name1, name2):
    """Hybrid similarity metric balancing common industry terms with unique identifiers"""
    name1_clean, name2_clean = clean_name(name1), clean_name(name2)
    tokens1, tokens2 = tokenize_name(name1), tokenize_name(name2)
    
    # Slightly reduced list of common industry terms
    
    # Calculate standard similarity metrics
    seq_sim = sequence_similarity(name1_clean, name2_clean)
    jaccard_sim = jaccard_similarity(set(tokens1), set(tokens2))
    subset_bonus = subset_match(name1, name2)
    position_bonus = word_position_bonus(name1, name2)
    common_bonus = common_words_bonus(name1, name2)
    
    # Calculate meaningful common words (excluding common industry terms)
    meaningful_tokens1 = set(t for t in tokens1 if t not in common_industry_terms)
    meaningful_tokens2 = set(t for t in tokens2 if t not in common_industry_terms)
    meaningful_common = meaningful_tokens1.intersection(meaningful_tokens2)
    
    # Calculate common industry terms
    common_tokens = set(tokens1).intersection(set(tokens2))
    industry_common = set(t for t in common_tokens if t in common_industry_terms)
    
    # Apply specific penalty for the "one moon/almuhit alhadi" case
    # If they only share industry terms and have different distinctive words
    if common_tokens and len(industry_common) > 0 and len(meaningful_common) == 0:
        # Only reduce score for specific case, not eliminate completely
        seq_sim *= 0.5
        jaccard_sim *= 0.5
        position_bonus *= 0.5
    
    # Standard hybrid scoring 
    hybrid_score = (seq_sim * 0.25 + jaccard_sim * 0.3 + subset_bonus * 0.15 + 
                   position_bonus * 0.15 + common_bonus * 0.15)
    
    # Apply a less aggressive penalty for specific case
    if common_tokens and len(industry_common) / len(common_tokens) > 0.5 and len(meaningful_common) == 0:
        hybrid_score *= 0.7  # Moderate penalty
    
    return hybrid_score

def compare_names(df, threshold=0.6):
    """Find matching names in a DataFrame"""
    matches = []
    matchesx = []
    
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            name1, name2 = df.iloc[i]['name'], df.iloc[j]['name']
            similarity = calculate_name_similarity(name1, name2)
            
            if similarity >= threshold:
                matchesx.append({
                    'match': [name1, name2],
                    'Record 1': f"ID: {df.iloc[i].name}, Name: {name1}",
                    'Record 2': f"ID: {df.iloc[j].name}, Name: {name2}",
                    'Similarities': {
                        'name': f"{similarity:.2f}"
                    }
                })
                matches.append({
                    'Name 1': name1,
                    'Name 2': name2,
                    'Similarity': round(similarity, 3)
                })
    print(matches)
    return pd.DataFrame(matches), matchesx

# Example usage with the given names
df = pd.DataFrame({'name': [
    "litasco middle east dmcc",
    "litasco middle east"
    "dynamik trader", 
    "nari strength",
    "one moon marine services", 
    "alqutb alshamali marine",  # Example with less similarity
    "almuhit alhadi marine services",  # Example with less similarity
    "star voyages shipping services", 
    "uae shipping association",
    "star voyages",
    "vladimir putin", 
    "putin", 
    "president vladimir putin",
    "moon services"

    

    "John Smith",
    "Jon Smith",
    "Dr. John Smith",
    "John J. Smith",
    "Jonathan Smith",
    "Johnny Smith",
    "Sarah Jones",
    "Michael Johnson"
]})

# Compare names and find matches
matchesy, matchesd = compare_names(df, threshold=0.5)  # You can adjust threshold as needed

# Display results
