import json

input_file = "entity_summary1.json"
with open(input_file, 'r') as f:
    entities = json.load(f)
    print(entities)
