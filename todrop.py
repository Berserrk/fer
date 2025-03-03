from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load Phi-4 model and tokenizer
model_name = "microsoft/Phi-4"
device = "mps" if torch.backends.mps.is_available() else "cpu"  # Use Apple MPS if available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Dictionary of entities and descriptions
entities = {
    "Company X": "Involved in fraudulent accounting practices and money laundering.",
    "Person Y": "Accused of insider trading but later acquitted.",
    "Organization Z": "Suspected of financing illegal activities but not yet proven.",
}

# Loop through each entity
for entity, description in entities.items():
    prompt = f"Analyze the following case:\nEntity: {entity}\nDescription: {description}\n\nBased on this information, has the entity committed a crime? Provide reasoning."

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate response
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=200)

    # Decode response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Print results
    print(f"**{entity}**:\n{response}\n{'-'*50}")
