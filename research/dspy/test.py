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

    # Override __call__ to intercept and process any unwanted keyword arguments (like "messages")
    def __call__(self, *args, **kwargs):
        if 'messages' in kwargs:
            messages = kwargs.pop('messages')
            # If messages is a list, join their "content" or string forms
            if isinstance(messages, list):
                prompt_parts = []
                for msg in messages:
                    if isinstance(msg, dict) and "content" in msg:
                        prompt_parts.append(msg["content"])
                    else:
                        prompt_parts.append(str(msg))
                new_prompt = "\n".join(prompt_parts)
            else:
                new_prompt = str(messages)
            # Replace the first positional argument (the prompt) with our constructed prompt
            if args:
                args = (new_prompt,) + args[1:]
            else:
                args = (new_prompt,)
        # Now call forward without the extra "messages" key in kwargs
        return self.forward(*args, **kwargs)

    def forward(self, prompt: str, **kwargs):
        return generate_response(prompt, **kwargs)

# Configure DSPy to use your custom language model
dspy.settings.configure(lm=MyHFLM())

# Function to parse the plain text response into DSPy's expected structured format
def parse_model_output(response_text):
    structured_response = {
        "choices": [
            {
                "message": {
                    "content": response_text.strip()
                }
            }
        ]
    }
    return structured_response

# Define and run a DSPy prediction task
qa_signature = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_signature)

try:
    # Run a DSPy prediction task; DSPy may send a "messages" argument internally.
    result = qa(question="What is the capital of France?")
    # Manually wrap the raw result into the structure DSPy expects.
    structured_output = parse_model_output(result)
    answer = structured_output["choices"][0]["message"]["content"]
    print("Answer:", answer)
except Exception as e:
    print("Error running DSPy task:", e)
