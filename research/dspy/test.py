
###
import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Hugging Face model and tokenizer
model_name = "microsoft/phi-2"  # Replace with your specific model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Function to generate response
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

# Custom DSPy-compatible language model wrapper
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-2")  # Just a label for internal use

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        return generate_response(prompt, **kwargs)

# Configure DSPy to use your custom language model
dspy.settings.configure(lm=MyHFLM())

# Define and run a DSPy prediction task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

try:
    result = qa(question="What is the capital of France?")
    # Manually parse the output
    output_text = result  # Assuming result is a string
    if "Answer:" in output_text:
        answer = output_text.split("Answer:")[1].strip()
    else:
        answer = output_text.strip()
    print("Answer:", answer)
except Exception as e:
    print(f"Error running DSPy task: {e}")








    ####
import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class HuggingFaceLM(dspy.LM):
    def __init__(self, model_name, hf_token=None, **kwargs):
        super().__init__(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token, device_map="auto")
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.kwargs = kwargs  # Store kwargs for generation parameters like temperature, max_tokens

    def __call__(self, prompt, **call_kwargs):
        # Combine default kwargs with call-specific kwargs
        generation_kwargs = {**self.kwargs, **call_kwargs}
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, **generation_kwargs)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return [dspy.Prediction(completion=response)]

# Usage
model_name = "meta-llama/Llama-2-7b-hf"
hf_token = "your_huggingface_token"  # Replace with your actual token
hf_lm = HuggingFaceLM(model_name, hf_token=hf_token, temperature=0.7, max_tokens=512)
dspy.settings.configure(lm=hf_lm)

# Define DSPy task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

# Test the setup
result = qa(question="What is the capital of France?")
print("Answer:", result.answer)