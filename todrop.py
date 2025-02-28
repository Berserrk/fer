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
    ('John Doe', 'Garamyov Enterprises'),
    ('Desmond', 'Desnodi'),
    ('Michael Smith', 'Rosneck Inc'),
    ('Richard Lee', 'Acme Corp'),
    ('Jane Doe', 'Rosneck Inc'),
    ('Alice Johnson', 'Global Tech'),
    ('Acme Corp', 'Beta Industries'),
    ('InvestorX', 'StartUpAlpha'),
    ('PartnerA', 'PartnerB'),
    ('Robert Brown', 'Criminal Enterprises')
]

# Descriptions of entities
desc_dic = {
    "John Doe": "John Doe is a businessman who owns a portion of Garamyov Enterprises.",
    "Garamyov Enterprises": "Garamyov Enterprises is a company flagged for involvement in money laundering.",
    "Desmond": "Desmond has committed money laundering activities.",
    "Desnodi": "Desnodi is an associate of Desmond, but has not committed any crimes.",
    "Michael Smith": "Michael Smith is an employee at Rosneck Inc and is not involved in any crimes.",
    "Rosneck Inc": "Rosneck Inc is a company sanctioned for money laundering and sanctions evasions.",
    "Richard Lee": "Richard Lee is the CEO of Acme Corp, an international corporation.",
    "Jane Doe": "Jane Doe is an investor and a business partner of Rosneck Inc.",
    "Alice Johnson": "Alice Johnson is the director of Global Tech, an enterprise working with various other companies.",
    "Global Tech": "Global Tech is a technology company focused on AI and machine learning.",
    "Acme Corp": "Acme Corp is a multinational corporation, working with Beta Industries in various projects.",
    "Beta Industries": "Beta Industries is a manufacturing company with a focus on construction and infrastructure.",
    "InvestorX": "InvestorX is a venture capitalist and has invested heavily in StartUpAlpha.",
    "StartUpAlpha": "StartUpAlpha is a tech startup, having recently received funding from InvestorX.",
    "PartnerA": "PartnerA is in a business partnership with PartnerB.",
    "PartnerB": "PartnerB is a business partner of PartnerA, involved in international trade.",
    "Robert Brown": "Robert Brown is a known criminal involved in various illicit activities with Criminal Enterprises.",
    "Criminal Enterprises": "Criminal Enterprises is a network involved in illegal trade and money laundering."
}

# Create a LLM prompt that will analyze the relationships
llm_prompt = f"""
You are a compliance assistant tasked with identifying the relationships between pairs of entities, such as individuals and companies. Your goal is to determine the type of relationship between the two entities and flag those who are involved in criminal activities. Use the descriptions provided for each entity to help you classify the relationship.

The relationship types to choose from are as follows:
{relationship_types}

The entities that have been flagged for crimes are:
{list_flagged}

You are provided with the following pairs of entities:
{abc}

Descriptions of the entities involved:
{desc_dic}

For each pair of entities, identify the type of relationship and determine:
1. The type of relationship between the two entities.
2. Which entity is the source and which is the target (the source is the entity with higher responsibility or influence).
3. Flag any entities involved in criminal activities based on their involvement in a crime.

Please provide the output in the following format:
- Entity1 - Entity2:
    - Relationship Type: [Type of relationship]
    - Source: [Source Entity]
    - Target: [Target Entity]
    - Flagged: [List of flagged entities involved]

Example format:
- John Doe - Garamyov Enterprises:
    - Relationship Type: Ownership
    - Source: Garamyov Enterprises
    - Target: John Doe
    - Flagged: ['Garamyov Enterprises']
"""

print(llm_prompt)
