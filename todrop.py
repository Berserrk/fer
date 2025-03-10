# Input dictionary
test1 = {
    "desc1": {
        "entities": ["entity1", "entity2"],
        "relationships": "OWNER",
        "reason": "the two entities are related"
    },
    "desc2": {
        "entities": ["entity3", "entity4"],
        "relationships": "OWNER",
        "reason": "the two entities are related"
    }
}

# Assign unique IDs to entities
entity_to_id = {}
current_id = 1

# Extract all unique entities and assign IDs
for desc in test1.values():
    for entity in desc["entities"]:
        if entity not in entity_to_id:
            entity_to_id[entity] = current_id
            current_id += 1

# Create node list
nodes = [{"data": {"id": id, "label": "ENTITY", "name": name}} for name, id in entity_to_id.items()]

# Create edge list
edges = [
    {
        "data": {
            "id": idx + 1,
            "label": desc["relationships"],
            "source": entity_to_id[desc["entities"][0]],
            "target": entity_to_id[desc["entities"][1]],
            "reason": desc["reason"]
        }
    }
    for idx, desc in enumerate(test1.values())
]

# Final structure
elements = {
    "nodes": nodes,
    "edges": edges
}

# Print output
import json
print(json.dumps(elements, indent=4))
