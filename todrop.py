
# Define the list of flagged entities
list_flagged = ['rosneck', "garamyov", "Desmond"]

# Define the relationships in abc
abc = [
    ('rikic', 'garamyov'),
    ('desmond', 'desnodi'),
    ('ase', 'rosneck')
]

# Descriptions of entities
desc_dic = {
    "rikic": "rikic has not committed any crime, he travelled to Dubai. He owns rosneck",
    "rosneck": "rosneck is a company sanctioned for money laundering and sanctions evasions",
    "Desmond": "Desmond has committed money laundering",
    "desnodi": "Desnodi has not committed any crimes. He is the associate of Desmond.",
    "ase": "ase is the victim of rosneck"
}

# Default description in case it's missing
default_description = "No description available for this entity."

# Define possible relationships to look for
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

def create_llm_prompt(abc, desc_dic):
    """
    Create an LLM prompt to extract relationship information between entities.
    Ensure all entities are described.
    """

    prompt = "Given the following descriptions and relationships between entities, extract the relationship type and determine if the entities are connected to a crime.\n\n"

    # Add the relationship information to the prompt
    for entity1, entity2 in abc:
        # Check if descriptions are missing and provide a default one
        description1 = desc_dic.get(entity1, default_description)
        description2 = desc_dic.get(entity2, default_description)
        
        prompt += f"Entities: {entity1} and {entity2}\n"
        prompt += f"Description of {entity1}: {description1}\n"
        prompt += f"Description of {entity2}: {description2}\n"
        prompt += "Relationship: "

        # Ask LLM to provide the relationship type
        prompt += f"Please classify the relationship between these entities as one of the following types: {', '.join(relationship_types)}.\n\n"

    prompt += """
Based on the relationships, flag any entities connected to a crime. For example, if one entity is involved in a crime (e.g., money laundering), flag all associated entities (e.g., owners, partners, associates) connected to the crime.

Please provide a list of flagged entities along with the type of relationship that resulted in the flagging and the reason for the flag. Flagging should be done based on potential involvement in a crime (e.g., money laundering, fraud, sanctions evasion, etc.).
"""
    return prompt


prompt = create_llm_prompt(abc, desc_dic)

# Use the LLM to analyze the relationships and flag entities
print(prompt)
# Display the flagged entities
