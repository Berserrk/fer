# Define the relationship types (categories of connections)
relationship_types = [
    'Ownership', 
    'Association', 
    'Criminal Involvement', 
    'Affiliation', 
    'Partnership',
    'Subcontracting', 
    'Beneficiary', 
    'Service Provider', 
    'Investment', 
    'Co-Conspirator'
]

# List of flagged entities (those involved in crime)
list_flagged = ['rosneck', 'garamyov', 'Desmond']

# Define the relationships in abc
abc = [
    ('rikic', 'garamyov'),
    ('desmond', 'desnodi'),
    ('ase', 'rosneck')
]

# Create the dictionary with flagged information
relationships = {}

for entity1, entity2 in abc:
    # Check if each entity is flagged
    flagged_info = {
        entity1: entity1 in list_flagged,
        entity2: entity2 in list_flagged
    }
    
    # Store the result in the dictionary
    relationships[(entity1, entity2)] = flagged_info

# Display the result
print(relationships)




You are a compliance assistant tasked with identifying the relationships between pairs of entities such as individuals and companies. Your goal is to determine the type of relationship between the two entities and flag any involved in criminal activities based on the given data.

The relationship types to choose from are as follows:
- Ownership
- Association
- Criminal Involvement
- Affiliation
- Partnership
- Subcontracting
- Beneficiary
- Service Provider
- Investment
- Co-Conspirator

Entities flagged for crimes are:
['rosneck', 'garamyov', 'Desmond']

For each pair of entities from the list of relationships below, determine the following:
1. The type of relationship between the two entities (choose from the predefined types).
2. Identify which entity is the source and which is the target. The source is the entity with higher responsibility or influence.
3. Flag any entities involved in criminal activities based on the information provided.

The relationships to evaluate:
[('rikic', 'garamyov'), ('desmond', 'desnodi'), ('ase', 'rosneck')]

Entities' crime involvement (based on list_flagged):
- rikic: Not flagged
- garamyov: Flagged
- desmond: Flagged
- desnodi: Not flagged
- ase: Not flagged
- rosneck: Flagged

Output your results in the following format:
- Entity1 - Entity2:
    - Relationship Type: [Type of relationship]
    - Source: [Source Entity]
    - Target: [Target Entity]
    - Flagged: [List of flagged entities involved]

For example:
- 'rikic' - 'garamyov':
    - Relationship Type: [Ownership]
    - Source: 'garamyov'
    - Target: 'rikic'
    - Flagged: ['garamyov']
