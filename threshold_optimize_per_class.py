# threshold_optimize_per_class.py
import numpy as np
import torch
from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.metrics import f1_score

labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust",
    "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
    "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]

print("📌 Loading test dataset...")
dataset = load_dataset("go_emotions")
test = dataset["test"]

print("📌 Loading tokenizer + model...")
tokenizer = DistilBertTokenizer.from_pretrained("./model")
model = DistilBertForSequenceClassification.from_pretrained("./model")

# test ifadelerini tokenize et
def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

print("📌 Tokenizing...")
test_enc = test.map(tokenize, batched=True)

# tensora çevir
input_ids = torch.tensor(test_enc["input_ids"])
attention_mask = torch.tensor(test_enc["attention_mask"])

# gerçek etiketler
num_labels = len(labels)
true_labels = np.zeros((len(test), num_labels))

for i, labs in enumerate(test["labels"]):
    row = [0.0] * num_labels
    for l in labs:
        row[l] = 1.0
    true_labels[i] = row

# Model logits
print("📌 Running model on test set...")
with torch.no_grad():
    logits = []
    bs = 32
    for i in range(0, len(test), bs):
        out = model(
            input_ids[i:i+bs],
            attention_mask=attention_mask[i:i+bs]
        )
        logits.append(out.logits)
    logits = torch.cat(logits).sigmoid().numpy()

print("📌 Optimizing thresholds per class...")

candidate_thresholds = np.arange(0.05, 0.51, 0.05)
best_thresholds = {}

for idx, label in enumerate(labels):
    best_f1 = 0
    best_t = 0.3  # fallback

    y_true = true_labels[:, idx]
    y_prob = logits[:, idx]

    for t in candidate_thresholds:
        y_pred = (y_prob > t).astype(int)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    best_thresholds[label] = best_t
    print(f"{label:15s}  best_t = {best_t:.2f}   f1 = {best_f1:.4f}")

print("\n🎉 DONE! Save this dictionary and use it in inference:\n")
print(best_thresholds)
