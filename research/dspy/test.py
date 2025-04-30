import json
import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ——— 1) Load your 4-bit Mistral (or Phi-4) model exactly as before ———
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/mistral-7B-instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.to(device)

# ——— 2) Plain‐text generation helper ———
def generate_response(prompt: str, max_length=200, temperature=0.7) -> str:
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length
    ).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            do_sample=True,
            temperature=temperature,
            top_p=0.9
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# ——— 3) DSPy LM wrapper that returns a JSON string with "text" ———
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model=model_name)  # label for logging

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        # ignore any extra kwargs like `messages`
        text = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 200),
            temperature=kwargs.get("temperature", 0.7)
        )
        # **return a JSON string containing "text"** so DSPy’s JSON‐fallback will accept it
        return json.dumps({"text": text})

# ——— 4) Tell DSPy to use this wrapper ———
dspy.settings.configure(lm=MyHFLM())

# ——— 5) Define & run your QA task ———
qa_sig = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_sig)

try:
    out = qa(question="What is the capital of France?")
    print("Answer:", out.answer)
except Exception as e:
    print("Error:", e)
