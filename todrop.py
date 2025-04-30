import dspy
from transformers import AutoTokenizer
from dspy import HFLocalModel

# Your local Phi-4 model path
model_path = "./phi4"

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Setup DSPy local model wrapper
local_lm = HFLocalModel(
    model=model_path,
    tokenizer=model_path,
    model_kwargs={
        "device_map": "auto",
        "load_in_4bit": True  # Remove if your model is full precision
    }
)

# Set the local model as the default LM for DSPy
dspy.settings.configure(lm=local_lm)

# Quick test program
class Summarizer(dspy.Signature):
    """A short summary of the input text."""
    text = dspy.InputField()
    summary = dspy.OutputField()

summarizer = dspy.Predict(Summarizer)
result = summarizer(text="The theory of relativity states that space and time are relative...")

print(result.summary)
