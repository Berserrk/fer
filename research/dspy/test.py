import json
import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ——— 1) Device + model loading ———
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/mistral-7B-instruct"
# model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/phi4"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model.to(device)

# ——— 2) Ensure a pad_token exists ———
if tokenizer.pad_token is None:
    # Use the eos token as padding
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

# ——— 3) Plain-text generation helper ———
def generate_response(
    prompt: str,
    max_length: int = 200,
    temperature: float = 0.7
) -> str:
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,           # now safe, because pad_token is defined
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

# ——— 4) DSPy LM wrapper that returns a dict with "text" ———
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model=model_name)

    @property
    def lm_type(self):
        return "completion"

    def __call__(self, *args, **kwargs):
        # DSPy might pass `question=` or `messages=`; grab whichever it gives
        if "question" in kwargs:
            prompt = kwargs.pop("question")
        elif args:
            prompt = args[0]
        else:
            prompt = ""

        # Generate the text
        text = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 200),
            temperature=kwargs.get("temperature", 0.7)
        )

        # Return a plain dict — DSPy’s JSON fallback will pick up `text`
        return {"text": text}

# ——— 5) Tell DSPy to use your custom LM ———
dspy.settings.configure(lm=MyHFLM())

# ——— 6) Signature & Predict ———
qa_sig = dspy.Signature("question -> text", "Answer the question concisely.")
qa = dspy.Predict(qa_sig)

# ——— 7) Run it ———
try:
    out = qa(question="What is the capital of Japan? Provide a concise answer.")
    print("Answer:", out.text)
except Exception as e:
    print("Error:", e)
