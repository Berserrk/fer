import json
import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 1) Load your HF model
model_name = "microsoft/phi-2"   # or "microsoft/phi-4" when available
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer.pad_token = tokenizer.eos_token

# 2) A helper that just returns plain text
def generate_response(prompt: str, max_length=512, temperature=0.7) -> str:
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
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# 3) Wrap it in a DSPy LM that returns a JSON string
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model="phi-4")   # internal label

    @property
    def lm_type(self):
        return "completion"

    def forward(self, prompt: str, **kwargs):
        # ignore any extra kwargs like 'messages'
        text = generate_response(prompt, **kwargs)
        # build the JSON that matches your signature's output field:
        return json.dumps({"answer": text})

# 4) Hook into DSPy
dspy.settings.configure(lm=MyHFLM())

# 5) Define and call your task
qa_sig = dspy.Signature("question -> answer", "Answer the question concisely.")
qa = dspy.Predict(qa_sig)

try:
    out = qa(question="What is the capital of France?")
    print("Answer:", out.answer)
except Exception as e:
    print("Error:", e)
