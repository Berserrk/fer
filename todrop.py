import pandas as pd

def create_bidirectional_df(data_dict):
   rows = []
   for entity, linked in data_dict.items():
       rows.append({
           'entity': entity, 
           'linked_entities': ', '.join(sorted(linked))  # Sort for consistent comparison
       })
       
       for linked_entity in linked:
           other_entities = [e for e in linked if e != linked_entity]
           if entity not in other_entities:
               other_entities.append(entity)
           rows.append({
               'entity': linked_entity,
               'linked_entities': ', '.join(sorted(other_entities))
           })
   
   # Create df and aggregate by entity
   df = pd.DataFrame(rows)
   df = df.groupby('entity')['linked_entities'].agg(lambda x: ', '.join(sorted(set(x.str.split(', ').sum())))).reset_index()
   
   return df

# Example 
data = {'entity1': ['entity2', 'entity3', 'entity2']}
df = create_bidirectional_df(data)
print(df)
