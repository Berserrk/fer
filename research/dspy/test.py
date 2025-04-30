import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load your Phi model
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer.pad_token = tokenizer.eos_token

# Plain text response generation function
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

# Custom DSPy LM wrapper
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-2")

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        return generate_response(prompt, **kwargs)

    def __call__(self, *args, **kwargs):
        if 'messages' in kwargs:
            messages = kwargs.pop('messages')
            if isinstance(messages, list):
                prompt = "\n".join([msg['content'] for msg in messages if isinstance(msg, dict) and 'content' in msg])
            else:
                prompt = str(messages)
            return self.forward(prompt, **kwargs)
        elif args:
            return self.forward(args[0], **kwargs)
        else:
            raise ValueError("No prompt provided.")

# Configure DSPy to use your custom LM
dspy.settings.configure(lm=MyHFLM())

# Define a DSPy module that relies on plain text output
class QuestionAnswerer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(dspy.Signature("question -> answer", "Answer the question concisely."))

    def forward(self, question):
        return self.predict(question=question)

# Instantiate and use the DSPy module
try:
    qa_model = QuestionAnswerer()
    result = qa_model(question="What is the capital of France?")
    print("Answer:", result.answer)
except Exception as e:
    print("Error running DSPy task:", e)
