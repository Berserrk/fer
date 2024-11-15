import json
from transformers import pipeline

# Load the JSON file
with open('entity_crimes.json', 'r') as f:
    entities = json.load(f)

# Define the list of labels
list_label = ['fraud', 'terrorism', 'money laundering', 'bribery or corruption', 'no label']

# Load the text classification model
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english', device=0)

# Process each entity in the JSON file
for entity_name, entity_description in entities.items():
    # Classify the entity description
    results = classifier(entity_description)
    
    # Get the label with the highest confidence score
    label = results[0]['label'].lower()
    
    # If the label is not in the list_label, use 'no label'
    if label not in list_label:
        label = 'no label'
        
    print(f"Entity: {entity_name}, Label: {label}")


prompt = "
You are a compliance officer tasked with evaluating whether an entity is committing a crime based on a provided description. Follow a step-by-step reasoning process to ensure your analysis is clear and thorough. Your goal is to determine:

    Whether the mentioned entity is directly involved in any criminal activity.
    If yes, classify the crime(s) using one or more of the following categories:
        Money Laundering
        Tax Evasion
        Terrorist Financing
        Criminal Organization
    If the entity is not directly involved in criminal activity, assess whether any associated parties or contextual elements should be flagged for potential risks.

Here’s the case for evaluation:
"The article does not explicitly mention EU as a specific entity, but it discusses several Cyprus-based financial service providers that offer services related to obtaining EU citizenship or residency through investments programs. These include Metriservus, ContecedSky, and Cypcodirect."

Your Task:
Use the following step-by-step process to evaluate:
Step-by-Step Instructions:

    Identify the Main Entity: Clearly identify the primary entity/entities mentioned in the description. Distinguish between the main subject (e.g., "EU") and associated entities (e.g., Cyprus-based providers).
    Evaluate Direct Criminal Involvement: Analyze whether the main entity (e.g., "EU") is explicitly involved in criminal activities based on the description.
    Assess Associated Risks: For any other mentioned entities (e.g., Metriservus, ContecedSky, Cypcodirect), determine if their activities might pose potential risks. Consider whether their actions align with the following crimes:
        Money Laundering: Facilitating illicit financial transactions or failing to conduct adequate due diligence.
        Tax Evasion: Assisting individuals in evading tax obligations through investment schemes.
        Terrorist Financing: Supporting or enabling the financing of terrorism.
        Criminal Organization: Participating in or facilitating activities related to organized crime.
    Provide Your Conclusion: Summarize the findings with clear labels for each entity and justification for the label.

Output Format:

    Step 1: Main Entity Identified: [Who is being analyzed?]
    Step 2: Direct Criminal Involvement: [Does the main entity commit a crime? If so, which one?]
    Step 3: Risks for Associated Parties: [Assess risks for related entities and classify crimes if applicable.]
    Final Conclusion:
        Entity: [Entity Name]
        Crime(s): [List of Crimes or "None"]
        Reasoning: [Detailed explanation of your decision.]
"