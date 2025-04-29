from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Set device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Local path to your Phi-4 model
model_path = "./phi4"  # Change this to your actual local path

# Load tokenizer and model from local directory
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

# Input prompt
input_text = "The theory of relativity states that"
input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

# Generate response
output_ids = model.generate(input_ids, max_length=100)
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(output_text)
