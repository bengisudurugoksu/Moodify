import json
import torch
import numpy as np
from datasets import load_dataset
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

print("🔍 Loading model, tokenizer, thresholds...")

tokenizer = BertTokenizer.from_pretrained("./modelsequence")
model = BertForSequenceClassification.from_pretrained("./modelsequence")
model.eval()

with open("./model/optimized_thresholds.json") as f:
    THRESHOLDS = json.load(f)

LABELS = [
  "admiration","amusement","anger","annoyance","approval","caring",
  "confusion","curiosity","desire","disappointment","disapproval","disgust",
  "embarrassment","excitement","fear","gratitude","grief","joy",
  "love","nervousness","optimism","pride","realization","relief",
  "remorse","sadness","surprise","neutral"
]

TOP_K = 3
MIN_CONFIDENCE = 0.15

RARE_FALLBACK = {
    "grief": "sadness",
    "relief": "neutral",
    "realization": "neutral"
}

dataset = load_dataset("go_emotions")
test = dataset["test"]

all_preds = []
all_labels = []

print(f"Evaluating on {len(test)} samples...")

for sample in test:
    text = sample["text"]
    true = sample["labels"]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits)[0]

    preds = [0] * 28

    text_len = len(text.split())
    length_penalty = 0.05 if text_len < 4 else 0.0

    scored = []

    for i, score in enumerate(probs):
        emotion = LABELS[i]
        threshold = THRESHOLDS.get(emotion, 0.3) + length_penalty
        score_val = score.item()

        if score_val >= threshold and score_val >= MIN_CONFIDENCE:
            scored.append((i, score_val))

    scored.sort(key=lambda x: x[1], reverse=True)
    scored = scored[:TOP_K]

    for idx, _ in scored:
        preds[idx] = 1

    gt = [0] * 28
    for l in true:
        gt[l] = 1

    all_preds.append(preds)
    all_labels.append(gt)

all_preds = np.array(all_preds)
all_labels = np.array(all_labels)

print("\n📊 FINAL METRICS (Inference-Time Optimized)")

print(f"Accuracy:  {accuracy_score(all_labels, all_preds):.4f}")
print(f"F1 Micro:  {f1_score(all_labels, all_preds, average='micro'):.4f}")
print(f"F1 Macro:  {f1_score(all_labels, all_preds, average='macro'):.4f}")
print(f"Precision: {precision_score(all_labels, all_preds, average='micro'):.4f}")
print(f"Recall:    {recall_score(all_labels, all_preds, average='micro'):.4f}")
