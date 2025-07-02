import re


with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
print("Total number of character:", len(raw_text))
print(raw_text[:99])

# tokenization of words
text = "Hello world. Is this-- a test?" 
result = re.split(r'(\s)', text)
print(result)

# We can remove whitespace but sometimes keeping them is relevant depending of the topic
# Removing them reduce memory and computing requirements.
result = re.split(r'([,.]|\s)', text)
print("taking into acount comma:",result)

result = [item for item in result if item.strip()]
print("removing whitespaces",result)

# modify to handle other types of punctuation
text = "Hello, world. Is this-- a test?"
result = re.split(r'([,.:;?_!"()\']|--|\s)', text)
result = [item.strip() for item in result if item.strip()]
print("more punctiations",result)

# apply it to entire edith warhton short story
preprocessed = re.split(r'([,.?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print(len(preprocessed))
print("show first 30 tokens",preprocessed[:30])



# Convert tokens into token ids
# create unique list of tokens
all_words = sorted(list(set(preprocessed)))
vocab_size = len(all_words)
print("vocab size:",vocab_size)

vocab = {token:integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item) 
    if i>50:
        break
print(vocab)

# Implementeing a simple text tokenizer: to encode and decode text
class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab #A
        self.int_to_str = {i:s for s,i in vocab.items()} #B
    
    def encode(self, text): #C
        preprocessed = re.split(r'([,.?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
        
    def decode(self, ids): #D
        text = " ".join([self.int_to_str[i] for i in ids]) 
        
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text) #E
        return text
    
tokenizer = SimpleTokenizerV1(vocab)
#encoder 
text = """"It's the last he painted, you know," Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text)
print(ids)

# decoder
print(tokenizer.decode(ids))