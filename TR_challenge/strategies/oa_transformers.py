# rag_classifier.py
import faiss
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    BertTokenizerFast, BertModel, BertForSequenceClassification,
    DPRContextEncoder, DPRContextEncoderTokenizerFast,
)
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import pandas as pd
import json

# ----- 1. Load and parse JSON lines -----
data = []
with open('../data/TRDataChallenge2023.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line: continue
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"Skipping line {i+1} due to parse error")

print(f"Loaded {len(data)} documents")

# ----- 2. Prepare DataFrame -----
df = pd.DataFrame(data)
df['postures'] = df['postures'].apply(lambda x: x if isinstance(x, list) else [])
def flatten_sections(secs):
    paragraphs = []
    for sec in secs:
        paragraphs.extend(sec.get('paragraphs', []))
    return ' '.join(paragraphs)
df['text'] = df['sections'].apply(flatten_sections)


import json
import faiss
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm
from transformers import BertTokenizerFast, BertForSequenceClassification, DPRContextEncoder, DPRContextEncoderTokenizerFast, Trainer, TrainingArguments

# Load and prepare data
df = pd.read_json('../data/TRDataChallenge2023.txt', lines=True)
df['postures'] = df['postures'].apply(lambda x: x if isinstance(x, list) else [])
def flatten_sections(secs):
    paragraphs = []
    for sec in secs:
        paragraphs.extend(sec.get('paragraphs', []))
    return ' '.join(paragraphs)
df['text'] = df['sections'].apply(flatten_sections)

# Encode labels
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df['postures'])
N_labels = len(mlb.classes_)

# Sample 1000 representative docs
from iterstrat.ml_stratifiers import MultilabelStratifiedShuffleSplit
msss = MultilabelStratifiedShuffleSplit(n_splits=1, test_size=(len(df) - 30)/len(df), random_state=42)
for train_idx, sample_idx in msss.split(df, Y):
    df = df.iloc[sample_idx]
    Y = Y[sample_idx]
df = df.reset_index(drop=True)

# Split data
train_df, val_df, Y_train, Y_val = train_test_split(df, Y, test_size=0.2, random_state=42)

# DPR encoder setup
dpr_tok = DPRContextEncoderTokenizerFast.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')
dpr_encoder = DPRContextEncoder.from_pretrained('facebook/dpr-ctx_encoder-single-nq-base')

train_texts = train_df['text'].tolist()
train_embs = []

batch_sz = 4
for i in tqdm(range(0, len(train_texts), batch_sz), desc="Encoding train embeddings"):
    batch = train_texts[i:i+batch_sz]
    toks = dpr_tok(batch, truncation=True, padding=True, max_length=256, return_tensors='pt')
    with torch.no_grad():
        embs = dpr_encoder(**toks).pooler_output.detach().cpu().numpy()
    train_embs.append(embs)

train_embs = np.vstack(train_embs)
dim = train_embs.shape[1]
index = faiss.IndexFlatIP(dim)
faiss.normalize_L2(train_embs)
index.add(train_embs)

# BERT classifier
bert_tok = BertTokenizerFast.from_pretrained('bert-base-uncased')
class RagClassifier(torch.nn.Module):
    def __init__(self, num_labels, n_neighbors=3):
        super().__init__()
        self.nbrs = n_neighbors
        self.dpr_encoder = dpr_encoder
        self.bert = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels, problem_type='multi_label_classification')

    def forward(self, input_ids, attention_mask, labels=None):
        with torch.no_grad():
            q_emb = self.dpr_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output
            q_emb = torch.nn.functional.normalize(q_emb, p=2, dim=1)
        sims, idxs = index.search(q_emb.cpu().numpy(), self.nbrs)

        batch_text = bert_tok.batch_decode(input_ids, skip_special_tokens=True)
        concat_texts = [
            qt + " [SEP] " + " [SEP] ".join(train_texts[j] for j in idxs_i)
            for qt, idxs_i in zip(batch_text, idxs)
        ]

        toks = bert_tok(concat_texts, truncation=True, padding=True, max_length=512, return_tensors='pt').to(input_ids.device)

        return self.bert(input_ids=toks['input_ids'], attention_mask=toks['attention_mask'], labels=labels)

# Dataset class
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        toks = self.tokenizer(self.texts[idx], truncation=True, padding='max_length', max_length=256, return_tensors='pt')
        item = {k: v.squeeze(0) for k, v in toks.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

train_ds = TextDataset(train_df['text'].tolist(), Y_train, bert_tok)
val_ds = TextDataset(val_df['text'].tolist(), Y_val, bert_tok)

# Training setup
model = RagClassifier(num_labels=N_labels, n_neighbors=3)
args = TrainingArguments(
    output_dir='rag_out',
    num_train_epochs=1,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    evaluation_strategy='epoch',
    learning_rate=2e-5,
    logging_dir='rag_logs',
)

trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=val_ds)
trainer.train()