Here's a Python solution to create the dataframe with bidirectional relationships:

```python
import pandas as pd

def create_bidirectional_df(data_dict):
    # Create initial dataframe
    df = pd.DataFrame([(k, ', '.join(v)) for k, v in data_dict.items()],
                     columns=['entity', 'linked_entities'])
    
    # Create additional rows for bidirectional relationships
    new_rows = []
    for entity, linked in data_dict.items():
        for linked_entity in linked:
            if linked_entity not in data_dict:
                # Get all entities that link to this one
                related = [e for e, l in data_dict.items() if linked_entity in l]
                new_rows.append({
                    'entity': linked_entity,
                    'linked_entities': ', '.join(related)
                })
    
    return pd.concat([df, pd.DataFrame(new_rows)]).drop_duplicates()

# Example usage
data = {
    'entity1': ['entity2', 'entity3']
}
df = create_bidirectional_df(data)
print(df)
```
