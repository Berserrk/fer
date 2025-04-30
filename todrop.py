import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Hugging Face model and tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Function to generate response
def generate_response(prompt, max_length=512, temperature=0.7):
    try:
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
    except Exception as e:
        print(f"Error in generation: {e}")
        return ""

# Create a DSPy-compatible LM wrapper
class MyHFLM(dspy.LM):
    def __call__(self, prompt, **kwargs):
        response = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        return dspy.Prediction(completion=response)

# Configure DSPy
dspy.settings.configure(lm=MyHFLM())

# Define and test DSPy task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

# Try generating an answer
try:
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print(f"Error running DSPy task: {e}")
