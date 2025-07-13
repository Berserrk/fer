from datasets import load_dataset

imdb = load_dataset("imdb")


from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Create a preprocessing function to tokenize text and truncate sequences to be no longer 
# than DistilBERT’s maximum input length:
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)


# Use 🤗 Datasets map function to apply the preprocessing function over the entire dataset. You can speed up the map
#  function by setting batched=True to process multiple elements of the dataset at once
tokenized_imdb = imdb.map(preprocess_function, batched=True)

#Use DataCollatorWithPadding to create a batch of examples. It will also dynamically pad 
# #your text to the length of the longest element in its batch, so they are a uniform length.
# While it is possible to pad your text in the tokenizer function by setting padding=True, dynamic padding is more efficient.

from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Load DistilBERT with AutoModelForSequenceClassification along with the number of expected labels:
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)





# Trainer will apply dynamic padding by default when you pass tokenizer to it. In this case, you don’t need to specify a data collator explicitly.
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_imdb["train"],
    eval_dataset=tokenized_imdb["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)
trainer.train()