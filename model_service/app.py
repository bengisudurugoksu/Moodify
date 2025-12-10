from fastapi import FastAPI
from pydantic import BaseModel
import torch
import json
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

app = FastAPI()

print("🚀 Loading model & tokenizer...")
tokenizer = DistilBertTokenizer.from_pretrained("../model")
model = DistilBertForSequenceClassification.from_pretrained("../model")
model.eval()

with open("thresholds.json") as f:
    THRESHOLDS = json.load(f)

LABELS = [
  "admiration","amusement","anger","annoyance","approval","caring",
  "confusion","curiosity","desire","disappointment","disapproval","disgust",
  "embarrassment","excitement","fear","gratitude","grief","joy",
  "love","nervousness","optimism","pride","realization","relief",
  "remorse","sadness","surprise","neutral"
]

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
        probs = torch.sigmoid(logits)[0]

    emotions = []
    for i, score in enumerate(probs):
        emotion = LABELS[i]
        threshold = THRESHOLDS.get(emotion, 0.3)

        if score.item() >= threshold:
            emotions.append({
                "name": emotion,
                "score": round(score.item(), 3)
            })

    emotions.sort(key=lambda x: x["score"], reverse=True)

    return {
        "emotions": emotions,
        "primaryEmotion": emotions[0]["name"] if emotions else "neutral"
    }
