import dspy
model="huggingface/meta-llama/Llama-3.2-3B-Instruct"
lm = dspy.LM(model=model, temperature=0.9, max_tokens=3000, stop=None, cache=False)
# Configure DSPy to use this LM
dspy.configure(lm=lm)
