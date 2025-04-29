import dspy
import json
import os  # Import the os module if you need to set environment variables

# --- 1. Configure the Language Model (Replace with your actual path) ---
local_model_path = "/path/to/your/local/llama/model"  # <--- REPLACE THIS WITH THE ACTUAL PATH

try:
    llama = dspy.LM(model=local_model_path, model_type="hf")
    dspy.settings.configure(lm=llama)
    print(f"Successfully loaded local Llama model from: {local_model_path}")
except Exception as e:
    print(f"Error loading the local Llama model: {e}")
    print("Please ensure the path to your local model is correct and that you have the necessary dependencies installed (torch, transformers).")
    exit()

# --- 2. Define the Signature for Structured Output ---
class StructuredAnswer(dspy.Signature):
    """Answer the question in a JSON format."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="JSON object with keys: 'capital' (string), 'population' (integer)")

# --- 3. Create a DSPy Module to Generate the Structured Answer ---
class GenerateStructuredAnswer(dspy.Module):
    def forward(self, question):
        prompt = f"""Answer the following question by providing a JSON object with the keys 'capital' and 'population'.

        Question: {question}
        Answer (JSON):"""
        return dspy.Predict(StructuredAnswer)(question=prompt)

# --- 4. Instantiate the DSPy Module ---
generator = GenerateStructuredAnswer()

# --- 5. Define the Question ---
my_question = "What is the capital and population of Switzerland?"

# --- 6. Generate the Prediction ---
prediction = generator(question=my_question)

# --- 7. Process and Print the Structured Answer ---
print(f"Question: {my_question}")
print(f"Raw Model Output: {prediction.answer}")

try:
    # Attempt to parse the model's output as JSON
    cleaned_output = prediction.answer.strip()
    if cleaned_output.startswith("{") and cleaned_output.endswith("}"):
        structured_answer = json.loads(cleaned_output)
        capital = structured_answer.get('capital')
        population = structured_answer.get('population')
        print("\nParsed Structured Answer:")
        print(f"Capital: {capital}")
        print(f"Population: {population}")
    else:
        print("\nWarning: Model output did not appear to be a valid JSON object.")
        print("Consider improving your prompt or adding more robust parsing.")
except json.JSONDecodeError as e:
    print(f"\nError parsing JSON: {e}")
    print("You need to carefully refine your prompt to ensure JSON output.")
