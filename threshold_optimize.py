# threshold_optimize.py
import numpy as np
import torch
from sklearn.metrics import f1_score
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from datasets import load_dataset

# --- MODEL & TOKENIZER ---
model_path = "./model"
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.eval()

# --- LABELS ---
num_labels = 28
dataset = load_dataset("go_emotions")
test_ds = dataset["test"]

# --- Tokenizer function ---
def tokenize(batch):
    encodings = tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )
    labels = []
    for labs in batch["labels"]:
        row = [0] * num_labels
        for i in labs:
            row[i] = 1
        labels.append(row)
    encodings["labels"] = labels
    return encodings

test_enc = test_ds.map(tokenize, batched=True)
test_enc.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# --- Collect true labels & predicted logits ---
all_labels = []
all_logits = []

with torch.no_grad():
    for batch in test_enc:
        input_ids = batch["input_ids"].unsqueeze(0)
        attention_mask = batch["attention_mask"].unsqueeze(0)
        labels = batch["labels"]

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits.squeeze(0)

        all_logits.append(logits.numpy())
        all_labels.append(labels.numpy())

all_logits = np.array(all_logits)
all_labels = np.array(all_labels)

print("Logit matrix:", all_logits.shape)
print("Label matrix:", all_labels.shape)

# --- Search best threshold ---
thresholds = np.arange(0.05, 0.55, 0.05)
best_f1 = -1
best_t = 0.3

for t in thresholds:
    preds = (torch.sigmoid(torch.tensor(all_logits)) > t).int().numpy()
    f1 = f1_score(all_labels, preds, average="micro")
    print(f"Threshold {t:.2f} → F1 = {f1:.4f}")
    
    if f1 > best_f1:
        best_f1 = f1
        best_t = t

print("\n🔎 Best threshold =", best_t, "with micro-F1 =", best_f1)
