import dspy
import os
from dspy.datasets import Example
from dspy.teleprompt import BootstrapFewShot

# Configure DSPy to use LLaMA-2-13B-chat via Together AI
together_api_key = os.environ.get("TOGETHER_API_KEY")
llama = dspy.LM(
    model='together_ai/togethercomputer/Llama-2-13B-chat',
    api_key=together_api_key,
    api_base="https://api.together.xyz/v1",
    max_tokens=500
)
dspy.settings.configure(lm=llama)

# Define representative example inputs
# These examples should be diverse, covering different reasoning patterns and domains
trainset = [
    Example(
        question="What is the capital city of the country where the inventor of the telephone was born?",
        answer="Ottawa",
        reasoning="The inventor of the telephone is Alexander Graham Bell, born in Scotland. Scotland is part of the United Kingdom, but Bell later moved to Canada, which is often associated with his work. However, since the question asks about his birth, the country is Scotland (UK). The capital of the UK is London. However, if we consider his significant contributions in Canada, the capital of Canada is Ottawa. Given the context, Ottawa is the more relevant answer."
    ),
    Example(
        question="Who was the president of the U.S. when the first moon landing occurred?",
        answer="Richard Nixon",
        reasoning="The first moon landing was Apollo 11 in July 1969. Richard Nixon was inaugurated as U.S. president in January 1969, so he was in office at the time."
    ),
    Example(
        question="What is the largest city in the country whose flag has a red maple leaf?",
        answer="Toronto",
        reasoning="The country with a red maple leaf on its flag is Canada. The largest city in Canada by population is Toronto."
    ),
    # Limited to 3 examples to simulate a low-data scenario (a limitation)
]

# Define a custom metric for evaluation
def exact_match_metric(example, pred, trace=None):
    """
    Metric to evaluate if the predicted answer exactly matches the ground truth.
    Returns True if the answers match (case-insensitive), False otherwise.
    """
    return example.answer.lower() == pred.answer.lower()

# Define the DSPy signature for multi-hop question answering
class MultiHopQA(dspy.Signature):
    """Answer a multi-hop question by reasoning through multiple steps."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Define the DSPy module using ChainOfThought
class MultiHopReasoner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(MultiHopQA)
    
    def forward(self, question):
        return self.generate(question=question)

# Initialize the module
reasoner = MultiHopReasoner()

# Optimize the pipeline using BootstrapFewShot
optimizer = BootstrapFewShot(
    metric=exact_match_metric,
    max_bootstrapped_demos=3,  # Use up to 3 demonstrations in prompts
    max_labeled_demos=3,       # Use all available examples
)
compiled_reasoner = optimizer.compile(
    reasoner,
    trainset=trainset
)

# Test the compiled pipeline
test_question = "What is the capital of the country where the inventor of the light bulb was born?"
result = compiled_reasoner(test_question)
print(f"Question: {test_question}")
print(f"Answer: {result.answer}")
print(f"Reasoning: {result.rationale}")

# Evaluate on a test example
test_example = Example(
    question=test_question,
    answer="Washington, D.C.",
    reasoning="The inventor of the light bulb is Thomas Edison, born in the United States. The capital of the U.S. is Washington, D.C."
)
evaluation = exact_match_metric(test_example, result)
print(f"Evaluation (Exact Match): {evaluation}")
