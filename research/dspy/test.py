import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load your Phi model (adjust model_name as needed, e.g., "microsoft/phi-4")
model_name = "microsoft/phi-2"  # Replace with your chosen model if different
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Function to generate a response from the model (plain text)
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
        temperature=temperature,
        do_sample=True,
        top_p=0.9
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Custom DSPy-compatible language model wrapper with __call__ override
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-2")  # Label for internal use

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        # We are now directly calling our plain text generation function
        return generate_response(prompt, **kwargs)

    # Override __call__ to handle DSPy's input structure
    def __call__(self, *args, **kwargs):
        if 'messages' in kwargs:
            messages = kwargs.pop('messages')
            if isinstance(messages, list):
                prompt_parts = [msg['content'] for msg in messages if isinstance(msg, dict) and 'content' in msg]
                prompt = "\n".join(prompt_parts)
            else:
                prompt = str(messages)
            return self.forward(prompt, **kwargs)
        elif args:
            return self.forward(args[0], **kwargs)
        else:
            raise ValueError("No prompt provided.")

# Configure DSPy to use your custom language model
dspy.settings.configure(lm=MyHFLM())

# Define and run a DSPy prediction task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

try:
    # Run a DSPy prediction task
    result = qa(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print("Error running DSPy task:", e)
