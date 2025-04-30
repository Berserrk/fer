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

# HF text generation function
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

# Custom DSPy-compatible wrapper
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="distilgpt2")

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        return generate_response(
            prompt,
            max_length=kwargs.get("max_length", 512),
            temperature=kwargs.get("temperature", 0.7)
        )

# Configure DSPy
dspy.settings.configure(lm=MyHFLM())

# Optional: Add simple output parser
class BasicAnswerParser(dspy.OutputParser):
    def parse(self, text: str):
        # Expect output like: "Answer: Paris"
        if "Answer:" in text:
            return {"answer": text.split("Answer:")[1].strip()}
        else:
            return {"answer": text.strip()}

# Define signature and model
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature, output_parser=BasicAnswerParser())

# Run the task
try:
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print(f"Error running DSPy task: {e}")



###test2
import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Phi model
model_name = "microsoft/phi-2"  # or "phi-3-mini", update to phi-4 when available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token  # for safe decoding

# Generate text from Phi
def generate_response(prompt, max_length=512, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True,
        top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# DSPy-compatible wrapper
class PhiLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-4")

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        return generate_response(prompt, **kwargs)

# Optional output parser
class SimpleAnswerParser(dspy.OutputParser):
    def parse(self, text: str):
        # Pull out "Answer: ..." from the raw text
        if "Answer:" in text:
            return {"answer": text.split("Answer:")[1].strip()}
        return {"answer": text.strip()}

# Set up DSPy
dspy.settings.configure(lm=PhiLM())

# Define and run a task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature, output_parser=SimpleAnswerParser())

try:
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print(f"Error running DSPy task: {e}")
