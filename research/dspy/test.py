import torch
import dspy
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1) Device + model loading
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "/domino/datasets/local/ArticleDetective_PreProd/models/mistral-7B-instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
# ensure pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id
model.to(device)

# 2) Plain-text generator
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
    # guard against empty outputs
    if outputs.numel() == 0:
        return ""
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# 3) DSPy LM wrapper returning a Prediction(text=...)
class MyHFLM(dspy.LM):
    def __init__(self):
        super().__init__(model=model_name)

    @property
    def lm_type(self):
        return "completion"

    def __call__(self, *args, **kwargs):
        # extract prompt from DSPy call signature
        if "question" in kwargs:
            prompt = kwargs["question"]
        elif args:
            prompt = args[0]
        elif "messages" in kwargs:
            msgs = kwargs["messages"]
            if isinstance(msgs, list):
                prompt = "\n".join(m.get("content", str(m)) if isinstance(m, dict) else str(m) for m in msgs)
            else:
                prompt = str(msgs)
        else:
            prompt = ""

        text = generate_response(
            prompt,
            max_length=kwargs.get("max_length", 200),
            temperature=kwargs.get("temperature", 0.7)
        )

        # return a Prediction object with a 'text' field
        return dspy.Prediction(text=text)

# 4) Hook it up
dspy.settings.configure(lm=MyHFLM())

# 5) Use a signature that maps question->text
qa_sig = dspy.Signature("question -> text", "Answer the question concisely.")
qa = dspy.Predict(qa_sig)

# 6) Run and print
try:
    out = qa(question="What is the capital of France?")
    print("Answer:", out.text)
except Exception as e:
    print("Error:", e)
