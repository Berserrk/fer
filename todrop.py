import dspy
import dspy

# Define the signature of your question-answering task
class QuestionAnswering(dspy.Signature):
    """Answer questions based on the provided context."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create a predictor module
predictor = dspy.Predict(QuestionAnswering)

# Your question
my_question = "What is the population of Switzerland?"

# Call the predictor with your question
prediction = predictor(question=my_question)

# The answer will be in the 'answer' field of the prediction
answer = prediction.answer

# Print the question and the answer
print(f"Question: {my_question}")
print(f"Answer: {answer}")
# Define the signature of your question-answering task
class QuestionAnswering(dspy.Signature):
    """Answer questions based on the provided context."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create a predictor module
predictor = dspy.Predict(QuestionAnswering)

# Your question
my_question = "What is the population of Switzerland?"

# Call the predictor with your question
prediction = predictor(question=my_question)

# The answer will be in the 'answer' field of the prediction
answer = prediction.answer

# Print the question and the answer
print(f"Question: {my_question}")
print(f"Answer: {answer}")
