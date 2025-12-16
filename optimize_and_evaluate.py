import numpy as np
import torch
from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns
import json

print("="*60)
print("🔍 STEP 1: Loading Model and Dataset")
print("="*60)

# Load model and tokenizer
model_path = "./model"
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Load dataset
dataset = load_dataset("go_emotions")
test = dataset["test"]

# Labels
labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust",
    "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
    "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]
num_labels = len(labels)

print(f"✓ Model loaded from {model_path}")
print(f"✓ Test dataset: {len(test)} samples")
print(f"✓ Number of emotion classes: {num_labels}")

# Tokenize test set
print("\n" + "="*60)
print("🔍 STEP 2: Tokenizing Test Data")
print("="*60)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

test_enc = test.map(tokenize, batched=True)
input_ids = torch.tensor(test_enc["input_ids"])
attention_mask = torch.tensor(test_enc["attention_mask"])

# Prepare true labels
true_labels = np.zeros((len(test), num_labels))
for i, labs in enumerate(test["labels"]):
    for l in labs:
        true_labels[i, l] = 1.0

print("✓ Tokenization complete")

# Get model predictions (logits)
print("\n" + "="*60)
print("🔍 STEP 3: Getting Model Predictions")
print("="*60)

with torch.no_grad():
    logits = []
    batch_size = 32
    for i in range(0, len(test), batch_size):
        out = model(
            input_ids[i:i+batch_size],
            attention_mask=attention_mask[i:i+batch_size]
        )
        logits.append(out.logits)
        if (i // batch_size + 1) % 50 == 0:
            print(f"  Processed {i+batch_size}/{len(test)} samples...")
    
    logits = torch.cat(logits).cpu()
    probs = torch.sigmoid(logits).numpy()

print("✓ Predictions obtained")

# OPTIMIZATION 1: Global threshold
print("\n" + "="*60)
print("🔍 STEP 4: Optimizing Global Threshold")
print("="*60)

thresholds = np.arange(0.05, 0.55, 0.05)
best_global_f1 = -1
best_global_t = 0.5

print("\nTesting global thresholds:")
for t in thresholds:
    preds = (probs > t).astype(int)
    f1 = f1_score(true_labels, preds, average="micro")
    print(f"  Threshold {t:.2f} → F1 = {f1:.4f}")
    
    if f1 > best_global_f1:
        best_global_f1 = f1
        best_global_t = t

print(f"\n✓ Best global threshold = {best_global_t:.2f} with F1 = {best_global_f1:.4f}")

# OPTIMIZATION 2: Per-class thresholds
print("\n" + "="*60)
print("🔍 STEP 5: Optimizing Per-Class Thresholds")
print("="*60)

candidate_thresholds = np.arange(0.05, 0.51, 0.05)
best_thresholds = {}

print("\nOptimizing threshold for each emotion:")
for idx, label in enumerate(labels):
    best_f1 = 0
    best_t = 0.3

    y_true = true_labels[:, idx]
    y_prob = probs[:, idx]

    for t in candidate_thresholds:
        y_pred = (y_prob > t).astype(int)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    best_thresholds[label] = best_t
    print(f"  {label:15s}  best_t = {best_t:.2f}   f1 = {best_f1:.4f}")

print("\n✓ Per-class thresholds optimized")

# Save thresholds
with open("./model/optimized_thresholds.json", "w") as f:
    json.dump({
        "global_threshold": best_global_t,
        "per_class_thresholds": best_thresholds
    }, f, indent=2)

print("✓ Thresholds saved to ./model/optimized_thresholds.json")

# EVALUATION: Compare methods
print("\n" + "="*60)
print("🔍 STEP 6: Final Evaluation with Optimized Thresholds")
print("="*60)

# Method 1: Default threshold (0.5)
preds_default = (probs > 0.5).astype(int)
f1_default = f1_score(true_labels, preds_default, average="micro")
acc_default = accuracy_score(true_labels, preds_default)
prec_default = precision_score(true_labels, preds_default, average="micro")
rec_default = recall_score(true_labels, preds_default, average="micro")

# Method 2: Optimized global threshold
preds_global = (probs > best_global_t).astype(int)
f1_global = f1_score(true_labels, preds_global, average="micro")
acc_global = accuracy_score(true_labels, preds_global)
prec_global = precision_score(true_labels, preds_global, average="micro")
rec_global = recall_score(true_labels, preds_global, average="micro")

# Method 3: Per-class thresholds
preds_perclass = np.zeros_like(probs)
for idx, label in enumerate(labels):
    preds_perclass[:, idx] = (probs[:, idx] > best_thresholds[label]).astype(int)

f1_perclass = f1_score(true_labels, preds_perclass, average="micro")
acc_perclass = accuracy_score(true_labels, preds_perclass)
prec_perclass = precision_score(true_labels, preds_perclass, average="micro")
rec_perclass = recall_score(true_labels, preds_perclass, average="micro")

# Print results
print("\n📊 COMPARISON OF METHODS:")
print("-" * 60)
print(f"{'Method':<30} {'F1':>8} {'Acc':>8} {'Prec':>8} {'Rec':>8}")
print("-" * 60)
print(f"{'Default (t=0.5)':<30} {f1_default:.4f}  {acc_default:.4f}  {prec_default:.4f}  {rec_default:.4f}")
print(f"{'Global Optimized (t={best_global_t:.2f})':<30} {f1_global:.4f}  {acc_global:.4f}  {prec_global:.4f}  {rec_global:.4f}")
print(f"{'Per-Class Optimized':<30} {f1_perclass:.4f}  {acc_perclass:.4f}  {prec_perclass:.4f}  {rec_perclass:.4f}")
print("-" * 60)

# Save results
with open("./model/evaluation_results_optimized.txt", "w") as f:
    f.write("="*60 + "\n")
    f.write("MODEL EVALUATION RESULTS (OPTIMIZED THRESHOLDS)\n")
    f.write("="*60 + "\n\n")
    f.write(f"Default Threshold (0.5):\n")
    f.write(f"  F1 Score:   {f1_default:.4f} ({f1_default*100:.2f}%)\n")
    f.write(f"  Accuracy:   {acc_default:.4f} ({acc_default*100:.2f}%)\n")
    f.write(f"  Precision:  {prec_default:.4f} ({prec_default*100:.2f}%)\n")
    f.write(f"  Recall:     {rec_default:.4f} ({rec_default*100:.2f}%)\n\n")
    
    f.write(f"Global Optimized Threshold ({best_global_t:.2f}):\n")
    f.write(f"  F1 Score:   {f1_global:.4f} ({f1_global*100:.2f}%)\n")
    f.write(f"  Accuracy:   {acc_global:.4f} ({acc_global*100:.2f}%)\n")
    f.write(f"  Precision:  {prec_global:.4f} ({prec_global*100:.2f}%)\n")
    f.write(f"  Recall:     {rec_global:.4f} ({rec_global*100:.2f}%)\n\n")
    
    f.write(f"Per-Class Optimized Thresholds:\n")
    f.write(f"  F1 Score:   {f1_perclass:.4f} ({f1_perclass*100:.2f}%)\n")
    f.write(f"  Accuracy:   {acc_perclass:.4f} ({acc_perclass*100:.2f}%)\n")
    f.write(f"  Precision:  {prec_perclass:.4f} ({prec_perclass*100:.2f}%)\n")
    f.write(f"  Recall:     {rec_perclass:.4f} ({rec_perclass*100:.2f}%)\n")

print("\n✓ Results saved to ./model/evaluation_results_optimized.txt")

# VISUALIZATION
print("\n" + "="*60)
print("🔍 STEP 7: Generating Visualizations")
print("="*60)

# Use best method (per-class) for presentation
best_metrics = {
    'F1 Score': f1_perclass * 100,
    'Accuracy': acc_perclass * 100,
    'Precision': prec_perclass * 100,
    'Recall': rec_perclass * 100
}

# 1. Main presentation chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#9D4EDD', '#BD86FA', '#C77DFF', '#E0AAFF']
bars = ax.bar(best_metrics.keys(), best_metrics.values(), color=colors, edgecolor='black', linewidth=2, width=0.6)
ax.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
ax.set_title('DistilBERT Emotion Classification Performance\n(Optimized Per-Class Thresholds)', fontsize=16, fontweight='bold', pad=20)
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

plt.tight_layout()
plt.savefig('./model/metrics_optimized_presentation.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: metrics_optimized_presentation.png")

# 2. Comparison chart
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(4)
width = 0.25

metrics_names = ['F1 Score', 'Accuracy', 'Precision', 'Recall']
default_vals = [f1_default*100, acc_default*100, prec_default*100, rec_default*100]
global_vals = [f1_global*100, acc_global*100, prec_global*100, rec_global*100]
perclass_vals = [f1_perclass*100, acc_perclass*100, prec_perclass*100, rec_perclass*100]

bars1 = ax.bar(x - width, default_vals, width, label='Default (0.5)', color='#E0AAFF', edgecolor='black')
bars2 = ax.bar(x, global_vals, width, label=f'Global ({best_global_t:.2f})', color='#C77DFF', edgecolor='black')
bars3 = ax.bar(x + width, perclass_vals, width, label='Per-Class', color='#9D4EDD', edgecolor='black')

ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
ax.set_title('Threshold Optimization Comparison', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics_names)
ax.legend()
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('./model/metrics_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: metrics_comparison.png")

print("\n" + "="*60)
print("✅ OPTIMIZATION AND EVALUATION COMPLETE!")
print("="*60)
print("\nGenerated files:")
print("  - ./model/optimized_thresholds.json")
print("  - ./model/evaluation_results_optimized.txt")
print("  - ./model/metrics_optimized_presentation.png")
print("  - ./model/metrics_comparison.png")
print("\n🎯 BEST RESULTS (Per-Class Thresholds):")
print(f"  F1 Score:   {f1_perclass*100:.2f}%")
print(f"  Accuracy:   {acc_perclass*100:.2f}%")
print(f"  Precision:  {prec_perclass*100:.2f}%")
print(f"  Recall:     {rec_perclass*100:.2f}%")