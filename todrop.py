
def create_bidirectional_df(data_dict):
    rows = []
    for entity, linked in data_dict.items():
        rows.append({
            'entity': entity, 
            'linked_entities': ', '.join(linked)
        })
        
        # Add rows for linked entities
        for linked_entity in linked:
            other_entities = [e for e in linked if e != linked_entity]
            if entity not in other_entities:
                other_entities.append(entity)
            rows.append({
                'entity': linked_entity,
                'linked_entities': ', '.join(other_entities)
            })
            
    return pd.DataFrame(rows).drop_duplicates()

# Example
data = {'entity1': ['entity2', 'entity3']}
df = create_bidirectional_df(data)
print(df)
