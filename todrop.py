# pip install dspy transformers torch

import dspy
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Step 1: Define your custom LLM wrapper
class LocalLLaMALM(dspy.LM):
    def __init__(self):
        # Replace with your own local path
        model_path = "/path/to/your/local/llama-model"

        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)

        # Create the generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0,  # 0 for GPU, -1 for CPU
            max_new_tokens=100
        )

    def __call__(self, prompt, **kwargs):
        output = self.generator(prompt, **kwargs)
        return output[0]["generated_text"]

# Step 2: Configure DSPy to use your offline LLaMA
dspy.settings.configure(lm=LocalLLaMALM())

# Step 3: Create a simple predictor using DSPy
predictor = dspy.Predict("question -> answer")

# Step 4: Ask a question
result = predictor(question="What is the capital of Germany?")
print("Answer:", result.answer)
