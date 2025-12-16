import json
import torch
import numpy as np
import matplotlib.pyplot as plt
from datasets import load_dataset
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from transformers import (
    DistilBertTokenizer, DistilBertForSequenceClassification,
    BertTokenizer, BertForSequenceClassification
)

# =========================
# CONFIG
# =========================
DISTIL_MODEL_PATH = "./model"        # DistilBERT
BERT_MODEL_PATH   = "./modelsequence"   # BERT-base
THRESHOLD_PATH    = "./model/optimized_thresholds.json"

TOP_K = 3
MIN_CONFIDENCE = 0.15
LABELS = [
    "admiration","amusement","anger","annoyance","approval","caring",
    "confusion","curiosity","desire","disappointment","disapproval","disgust",
    "embarrassment","excitement","fear","gratitude","grief","joy",
    "love","nervousness","optimism","pride","realization","relief",
    "remorse","sadness","surprise","neutral"
]

# =========================
# LOAD DATA
# =========================
print("🔍 Loading GoEmotions test set...")
dataset = load_dataset("go_emotions")
test = dataset["test"]

with open(THRESHOLD_PATH) as f:
    THRESHOLDS = json.load(f)

# =========================
# INFERENCE EVALUATION
# =========================
def evaluate_model(model, tokenizer, model_name):
    print(f"\n🚀 Evaluating {model_name} ...")

    all_preds, all_labels = [], []

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
            threshold = THRESHOLDS.get(LABELS[i], 0.3) + length_penalty
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

    metrics = {
        "Accuracy": accuracy_score(all_labels, all_preds) * 100,
        "Precision": precision_score(all_labels, all_preds, average="micro") * 100,
        "Recall": recall_score(all_labels, all_preds, average="micro") * 100,
        "F1_micro": f1_score(all_labels, all_preds, average="micro") * 100,
        "F1_macro": f1_score(all_labels, all_preds, average="macro") * 100,
        "F1_weighted": f1_score(all_labels, all_preds, average="weighted") * 100,
    }

    return metrics

# =========================
# LOAD MODELS
# =========================
print("\n📦 Loading models...")

distil_tokenizer = DistilBertTokenizer.from_pretrained(DISTIL_MODEL_PATH)
distil_model = DistilBertForSequenceClassification.from_pretrained(DISTIL_MODEL_PATH)
distil_model.eval()

bert_tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH)
bert_model = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.eval()

# =========================
# RUN EVALUATION
# =========================
distil_metrics = evaluate_model(distil_model, distil_tokenizer, "DistilBERT")
bert_metrics   = evaluate_model(bert_model, bert_tokenizer, "BERT-base")

def plot_single_model(metrics, model_name, filename, color):
    labels_main = ["F1_micro", "Accuracy", "Precision", "Recall"]

    fig = plt.figure(figsize=(18, 12))

    # --- 1. Main Performance Metrics ---
    ax1 = plt.subplot(2, 2, 1)
    values = [metrics[k] for k in labels_main]

    ax1.bar(["F1", "Accuracy", "Precision", "Recall"], values,
            color=color, edgecolor="black")
    ax1.set_ylim(0, 100)
    ax1.set_title(f"{model_name} – Main Performance Metrics")
    ax1.set_ylabel("Score (%)")
    ax1.grid(axis="y", alpha=0.3)

    # --- 2. F1 Comparison ---
    ax2 = plt.subplot(2, 2, 2)
    f1_vals = [
        metrics["F1_micro"],
        metrics["F1_macro"],
        metrics["F1_weighted"]
    ]

    ax2.bar(["Micro", "Macro", "Weighted"], f1_vals,
            color=color, edgecolor="black")
    ax2.set_ylim(0, 100)
    ax2.set_title(f"{model_name} – F1 Score Comparison")
    ax2.set_ylabel("F1 Score (%)")
    ax2.grid(axis="y", alpha=0.3)

    # --- 3. Radar Chart ---
    ax3 = plt.subplot(2, 2, 3, polar=True)
    radar_labels = ["F1", "Accuracy", "Precision", "Recall"]
    angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False)
    angles = np.concatenate([angles, [angles[0]]])

    radar_vals = values + values[:1]

    ax3.plot(angles, radar_vals, color=color, linewidth=2)
    ax3.fill(angles, radar_vals, alpha=0.3, color=color)
    ax3.set_thetagrids(angles[:-1] * 180/np.pi, radar_labels)
    ax3.set_ylim(0, 100)
    ax3.set_title(f"{model_name} – Performance Radar")

    # --- 4. Table ---
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis("off")

    table_data = [
        ["Metric", "Score"],
        ["F1 (Micro)", f"{metrics['F1_micro']:.2f}%"],
        ["F1 (Macro)", f"{metrics['F1_macro']:.2f}%"],
        ["Accuracy", f"{metrics['Accuracy']:.2f}%"],
        ["Precision", f"{metrics['Precision']:.2f}%"],
        ["Recall", f"{metrics['Recall']:.2f}%"],
    ]

    table = ax4.table(cellText=table_data[1:],
                      colLabels=table_data[0],
                      loc="center",
                      cellLoc="center")
    table.scale(1, 2)
    ax4.set_title(f"{model_name} – Detailed Summary")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

    print(f"✅ Saved: {filename}")

# =========================
# PLOTTING
# =========================
labels_main = ["F1_micro", "Accuracy", "Precision", "Recall"]

fig = plt.figure(figsize=(18, 12))

# --- 1. Main Performance Metrics ---
ax1 = plt.subplot(2, 2, 1)
x = np.arange(len(labels_main))
width = 0.35

ax1.bar(x - width/2, [distil_metrics[k] for k in labels_main],
        width, label="DistilBERT", color="#9D4EDD")
ax1.bar(x + width/2, [bert_metrics[k] for k in labels_main],
        width, label="BERT-base", color="#C77DFF")

ax1.set_xticks(x)
ax1.set_xticklabels(["F1", "Accuracy", "Precision", "Recall"])
ax1.set_ylim(0, 100)
ax1.set_title("Main Performance Metrics (Inference-Time)")
ax1.set_ylabel("Score (%)")
ax1.legend()
ax1.grid(axis="y", alpha=0.3)

# --- 2. F1 Comparison ---
ax2 = plt.subplot(2, 2, 2)
f1_labels = ["F1_micro", "F1_macro", "F1_weighted"]

ax2.bar(x[:3] - width/2, [distil_metrics[k] for k in f1_labels],
        width, label="DistilBERT", color="#9D4EDD")
ax2.bar(x[:3] + width/2, [bert_metrics[k] for k in f1_labels],
        width, label="BERT-base", color="#C77DFF")

ax2.set_xticks(x[:3])
ax2.set_xticklabels(["Micro", "Macro", "Weighted"])
ax2.set_ylim(0, 100)
ax2.set_title("F1 Score Comparison")
ax2.set_ylabel("F1 Score (%)")
ax2.legend()
ax2.grid(axis="y", alpha=0.3)

# --- 3. Radar Chart ---
ax3 = plt.subplot(2, 2, 3, polar=True)
radar_labels = ["F1_micro", "Accuracy", "Precision", "Recall"]
angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False)
angles = np.concatenate([angles, [angles[0]]])

distil_vals = [distil_metrics[k] for k in radar_labels]
bert_vals   = [bert_metrics[k] for k in radar_labels]
distil_vals += distil_vals[:1]
bert_vals   += bert_vals[:1]

ax3.plot(angles, distil_vals, label="DistilBERT", color="#9D4EDD")
ax3.fill(angles, distil_vals, alpha=0.25, color="#9D4EDD")
ax3.plot(angles, bert_vals, label="BERT-base", color="#C77DFF")
ax3.fill(angles, bert_vals, alpha=0.25, color="#C77DFF")

ax3.set_thetagrids(angles[:-1] * 180/np.pi, ["F1", "Acc", "Prec", "Rec"])
ax3.set_ylim(0, 100)
ax3.set_title("Performance Radar Chart")
ax3.legend(loc="upper right")

# --- 4. Table ---
ax4 = plt.subplot(2, 2, 4)
ax4.axis("off")

table_data = [
    ["Metric", "DistilBERT", "BERT-base"],
    ["F1 (Micro)", f"{distil_metrics['F1_micro']:.2f}%", f"{bert_metrics['F1_micro']:.2f}%"],
    ["F1 (Macro)", f"{distil_metrics['F1_macro']:.2f}%", f"{bert_metrics['F1_macro']:.2f}%"],
    ["Accuracy",   f"{distil_metrics['Accuracy']:.2f}%", f"{bert_metrics['Accuracy']:.2f}%"],
    ["Precision",  f"{distil_metrics['Precision']:.2f}%", f"{bert_metrics['Precision']:.2f}%"],
    ["Recall",     f"{distil_metrics['Recall']:.2f}%", f"{bert_metrics['Recall']:.2f}%"],
]

table = ax4.table(cellText=table_data[1:],
                  colLabels=table_data[0],
                  loc="center",
                  cellLoc="center")
table.scale(1, 2)
ax4.set_title("Detailed Performance Summary")

plt.tight_layout()
plt.savefig("distilbert_vs_bert_comparison.png", dpi=300)

# =========================
# SINGLE MODEL FIGURES
# =========================
plot_single_model(
    distil_metrics,
    model_name="DistilBERT (Baseline)",
    filename="distilbert_performance.png",
    color="#9D4EDD"
)

plot_single_model(
    bert_metrics,
    model_name="BERT-base (Final Model)",
    filename="bert_performance.png",
    color="#C77DFF"
)

print("\n✅ Saved: distilbert_vs_bert_comparison.png")
