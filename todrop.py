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
tokenizer.pad_token = tokenizer.eos_token  # Required for some decoding methods

# Function to generate a response from the model
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

# Custom DSPy-compatible language model wrapper
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="distilgpt2")  # Just a label for internal use

    @property
    def lm_type(self):
        return "completion"  # Tells DSPy this is a plain text completion model

    def forward(self, prompt: str, **kwargs):
        response = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 512),
            temperature=kwargs.get("temperature", 0.7)
        )
        return response

# Configure DSPy to use your custom language model
dspy.settings.configure(lm=MyHFLM())

# Define and run a DSPy prediction task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

try:
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print(f"Error running DSPy task: {e}")
