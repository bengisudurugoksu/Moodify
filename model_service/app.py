from fastapi import FastAPI
from pydantic import BaseModel
import torch
import json
from transformers import BertTokenizer, BertForSequenceClassification

app = FastAPI()

print("🚀 Loading BERT model & tokenizer...")

# 🔹 BERT-base model (friend model)
MODEL_PATH = "../modelsequence"   # <- BERT modelinin olduğu klasör

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# 🔹 Optimized thresholds
with open("thresholds.json") as f:
    THRESHOLDS = json.load(f)

LABELS = [
  "admiration","amusement","anger","annoyance","approval","caring",
  "confusion","curiosity","desire","disappointment","disapproval","disgust",
  "embarrassment","excitement","fear","gratitude","grief","joy",
  "love","nervousness","optimism","pride","realization","relief",
  "remorse","sadness","surprise","neutral"
]

# 🔧 Inference-time improvements (NO TRAINING)
TOP_K = 3
MIN_CONFIDENCE = 0.15

RARE_FALLBACK = {
    "grief": "sadness",
    "relief": "neutral",
    "realization": "neutral"
}

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(req: TextRequest):
    inputs = tokenizer(
        req.text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits)[0]  # multi-label → sigmoid

    emotions = []

    text_len = len(req.text.split())
    length_penalty = 0.05 if text_len < 4 else 0.0

    for i, score in enumerate(probs):
        emotion = LABELS[i]
        base_threshold = THRESHOLDS.get(emotion, 0.3)
        threshold = base_threshold + length_penalty

        score_val = round(score.item(), 3)

        if score_val >= threshold and score_val >= MIN_CONFIDENCE:
            emotions.append({
                "name": emotion,
                "score": score_val
            })

    # sort by confidence
    emotions.sort(key=lambda x: x["score"], reverse=True)

    # top-k
    emotions = emotions[:TOP_K]

    if emotions:
        primary = emotions[0]["name"]
        primary = RARE_FALLBACK.get(primary, primary)
    else:
        primary = "neutral"

    return {
        "emotions": emotions,
        "primaryEmotion": primary
    }
