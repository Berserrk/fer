import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Phi model (replace with your model if different)
model_name = "microsoft/phi-2"  # Example; change to Phi-4 or your specific model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Function to generate a response from the model (plain text)
def generate_response(prompt, max_length=512, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=temperature,
        do_sample=True,
        top_p=0.9
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

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

# Function to parse the raw model output into the expected structured format
def parse_model_output(response_text):
    # Manually create the structure DSPy expects:
    structured_response = {
        "choices": [
            {
                "message": {
                    "content": response_text.strip()  # Clean up response
                }
            }
        ]
    }
    return structured_response

# Define and run a DSPy prediction task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

try:
    # Run a task and get the plain text response from the model
    result = qa(question="What is the capital of France?")
    print(f"Raw result from DSPy: {result}")  # Debug the result from DSPy

    # Manually parse the output into the expected structure
    structured_output = parse_model_output(result)

    # Extract the answer from the structured response
    answer = structured_output["choices"][0]["message"]["content"]
    print(f"Answer: {answer}")

except Exception as e:
    print(f"Error running DSPy task: {e}")
