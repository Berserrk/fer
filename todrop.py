import dspy
import subprocess
import os
import logging
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalLLaMALM(dspy.LM):
    def __init__(self, model_path="/path/to/your/llama-model.gguf", **kwargs):
        super().__init__(model="local-llama", **kwargs)
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        self.kwargs = kwargs  # Store kwargs for DSPy compatibility

    def basic_request(self, prompt, **kwargs):
        # Merge kwargs from method call with stored kwargs
        request_kwargs = {**self.kwargs, **kwargs}

        # Write prompt to a temporary file to avoid shell injection
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(prompt)
            tmp_path = tmp.name

        # Build the command for the LLaMA CLI (adjust to your CLI tool)
        command = [
            "./llama.cpp/main",  # Replace with the actual path to your CLI tool
            "-m", self.model_path,
            "-f", tmp_path,  # Pass prompt via file
            "-n", str(request_kwargs.get("max_tokens", 100)),
            "--temp", str(request_kwargs.get("temperature", 0.7)),
            "--top-p", str(request_kwargs.get("top_p", 0.9))
        ]

        logger.info(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Return response in DSPy-compatible format
                return {"choices": [{"text": result.stdout.strip()}]}
            else:
                raise RuntimeError(f"Command failed: {result.stderr.strip()}")
        except FileNotFoundError:
            raise RuntimeError("LLaMA CLI tool not found. Ensure it is installed.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("LLaMA CLI command timed out.")
        finally:
            os.unlink(tmp_path)  # Clean up temporary file

    def __call__(self, prompt, **kwargs):
        # Ensure __call__ delegates to basic_request
        if not prompt:
            raise ValueError("Prompt is required for __call__")
        return self.basic_request(prompt, **kwargs)

# Configure DSPy to use the local LLaMA model
dspy.settings.configure(lm=LocalLLaMALM())

# Define a signature for the predictor
class QAPredictor(dspy.Signature):
    """Answer the question based on the input."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create and use the predictor
predictor = dspy.Predict(QAPredictor)
result = predictor(question="What is the capital of France?")
print("Answer:", result.answer)
