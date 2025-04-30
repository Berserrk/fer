import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Hugging Face model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"  # Replace with your model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Simple function to generate response with Hugging Face model
def generate_response(prompt, max_length=512, temperature=0.7):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length
    ).to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        temperature=temperature,
        top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Configure DSPy with a basic LM wrapper
def simple_lm(prompt, **kwargs):
    response = generate_response(prompt, max_length=kwargs.get("max_length", 512))
    return [dspy.Prediction(completion=response)]

dspy.settings.configure(lm=simple_lm)

# Define DSPy task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

# Test the setup
result = qa(question="What is the capital of France?")
print(result.answer)
