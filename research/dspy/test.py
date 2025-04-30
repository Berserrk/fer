import json
import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 1) Load your 4-bit model exactly as you had it
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/mistral-7B-instruct"
# model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/phi4"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.to(device)

# 2) A simple generator function
def generate_response(prompt: str, max_length=200, temperature=0.7) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            temperature=temperature,
            top_p=0.9
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# 3) Wrap it in a DSPy LM that returns a JSON string {"answer": "..."}
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model=model_name)  # internal label

    @property
    def lm_type(self):
        return "completion"  # treat as a plain completion model

    def forward(self, prompt: str, **kwargs):
        # ignore any extra kwargs DSPy might pass (e.g. messages)
        text = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 200),
            temperature=kwargs.get("temperature", 0.7)
        )
        # return a JSON string with exactly the field your signature needs
        return json.dumps({"answer": text})

# 4) Tell DSPy to use it
dspy.settings.configure(lm=MyHFLM())

# 5) Define and run your QA task
qa_sig = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_sig)

try:
    result = qa(question="What is the capital of Japan? Provide a concise and short answer")
    print("Answer:", result.answer)
except Exception as e:
    print("Error:", e)
