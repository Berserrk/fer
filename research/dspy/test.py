import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the Phi-4 model and tokenizer
model_name = "microsoft/phi-2"  # Replace with "microsoft/phi-4" if available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Function to generate a response from the model
def generate_response(prompt, max_length=512, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True,
        top_p=0.9
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()

# Custom DSPy-compatible language model wrapper
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-4")  # Label for internal use

    @property
    def lm_type(self):
        return "completion"

    def __call__(self, *args, **kwargs):
        # Extract and process 'messages' if present
        if 'messages' in kwargs:
            messages = kwargs.pop('messages')
            if isinstance(messages, list):
                prompt_parts = []
                for msg in messages:
                    if isinstance(msg, dict) and "content" in msg:
                        prompt_parts.append(msg["content"])
                    else:
                        prompt_parts.append(str(msg))
                prompt = "\n".join(prompt_parts)
            else:
                prompt = str(messages)
            args = (prompt,) + args[1:]
        return self.forward(*args, **kwargs)

    def forward(self, prompt: str, **kwargs):
        response_text = generate_response(prompt, **kwargs)
        # Wrap the response in the expected structured format
        return {
            "choices": [
                {
                    "message": {
                        "content": response_text
                    }
                }
            ]
        }

# Configure DSPy to use your custom language model
dspy.settings.configure(lm=MyHFLM())

# Define a DSPy signature
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

# Run a DSPy prediction task
try:
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print("Error running DSPy task:", e)
