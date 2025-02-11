import pandas as pd
from itertools import chain

def get_unique_pairs(df):
    # Create pairs from each row
    pairs = [(row['entity'], linked_entity) 
             for _, row in df.iterrows() 
             for linked_entity in row['linked_entities']]
    
    # Convert to set of frozensets to remove duplicates regardless of order
    unique_pairs = set(frozenset((a, b)) for a, b in pairs)
    
    # Convert back to list of tuples with consistent ordering
    result = [(tuple(pair)) for pair in unique_pairs]
    
    return result

# Example usage
data = {
    'entity': ['entity1', 'entity2'],
    'linked_entities': [['compA', 'entity2'], ['entity1', 'compB']]
}

df = pd.DataFrame(data)
pairs = get_unique_pairs(df)

# Print results
for pair in pairs:
    print(f"{pair[0]} - {pair[1]}")
