from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading model and dataset...")

# Load model
model = DistilBertForSequenceClassification.from_pretrained("./model")
tokenizer = DistilBertTokenizer.from_pretrained("./model")
model.eval()

# Load test dataset
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

print(f"Evaluating on {len(test)} test samples...")

# Prepare data
def tokenize_batch(texts):
    return tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")

# Run evaluation
all_preds = []
all_labels = []
batch_size = 32

with torch.no_grad():
    for i in range(0, len(test), batch_size):
        batch = test[i:i+batch_size]
        texts = batch["text"]
        true_labels = batch["labels"]
        
        # Tokenize
        inputs = tokenize_batch(texts)
        
        # Predict
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits)
        preds = (probs > 0.5).int().cpu().numpy()
        
        # Convert true labels to multi-hot encoding
        for labs in true_labels:
            row = [0] * 28
            for idx in labs:
                row[idx] = 1
            all_labels.append(row)
        
        all_preds.extend(preds)
        
        if (i // batch_size + 1) % 10 == 0:
            print(f"Processed {i+batch_size}/{len(test)} samples...")

all_preds = np.array(all_preds)
all_labels = np.array(all_labels)

print("\nCalculating metrics...")

# Calculate metrics
accuracy = accuracy_score(all_labels, all_preds)
f1_micro = f1_score(all_labels, all_preds, average='micro')
f1_macro = f1_score(all_labels, all_preds, average='macro')
f1_weighted = f1_score(all_labels, all_preds, average='weighted')
precision_micro = precision_score(all_labels, all_preds, average='micro')
precision_macro = precision_score(all_labels, all_preds, average='macro')
recall_micro = recall_score(all_labels, all_preds, average='micro')
recall_macro = recall_score(all_labels, all_preds, average='macro')

print("\n" + "="*60)
print("📊 MODEL EVALUATION RESULTS")
print("="*60)
print(f"Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"F1 Score (Micro):   {f1_micro:.4f} ({f1_micro*100:.2f}%)")
print(f"F1 Score (Macro):   {f1_macro:.4f} ({f1_macro*100:.2f}%)")
print(f"F1 Score (Weighted):{f1_weighted:.4f} ({f1_weighted*100:.2f}%)")
print(f"Precision (Micro):  {precision_micro:.4f} ({precision_micro*100:.2f}%)")
print(f"Precision (Macro):  {precision_macro:.4f} ({precision_macro*100:.2f}%)")
print(f"Recall (Micro):     {recall_micro:.4f} ({recall_micro*100:.2f}%)")
print(f"Recall (Macro):     {recall_macro:.4f} ({recall_macro*100:.2f}%)")
print("="*60)

# Save metrics to file
with open("./model/evaluation_results.txt", "w") as f:
    f.write("="*60 + "\n")
    f.write("MODEL EVALUATION RESULTS\n")
    f.write("="*60 + "\n")
    f.write(f"Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    f.write(f"F1 Score (Micro):   {f1_micro:.4f} ({f1_micro*100:.2f}%)\n")
    f.write(f"F1 Score (Macro):   {f1_macro:.4f} ({f1_macro*100:.2f}%)\n")
    f.write(f"F1 Score (Weighted):{f1_weighted:.4f} ({f1_weighted*100:.2f}%)\n")
    f.write(f"Precision (Micro):  {precision_micro:.4f} ({precision_micro*100:.2f}%)\n")
    f.write(f"Precision (Macro):  {precision_macro:.4f} ({precision_macro*100:.2f}%)\n")
    f.write(f"Recall (Micro):     {recall_micro:.4f} ({recall_micro*100:.2f}%)\n")
    f.write(f"Recall (Macro):     {recall_macro:.4f} ({recall_macro*100:.2f}%)\n")

print("\n✅ Results saved to ./model/evaluation_results.txt")

# Create visualizations
print("\nGenerating visualizations...")

# Metrics for main presentation
main_metrics = {
    'F1 Score': f1_micro * 100,
    'Accuracy': accuracy * 100,
    'Precision': precision_micro * 100,
    'Recall': recall_micro * 100
}

# 1. Main bar chart for presentation
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#9D4EDD', '#BD86FA', '#C77DFF', '#E0AAFF']
bars = ax.bar(main_metrics.keys(), main_metrics.values(), color=colors, edgecolor='black', linewidth=2, width=0.6)
ax.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
ax.set_title('DistilBERT Emotion Classification Performance', fontsize=16, fontweight='bold', pad=20)
ax.set_ylim([0, 100])
ax.axhline(y=90, color='red', linestyle='--', alpha=0.5, linewidth=2, label='90% Threshold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend(fontsize=12)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

plt.tight_layout()
plt.savefig('./model/metrics_presentation.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Saved: metrics_presentation.png")

# 2. Comprehensive visualization
fig = plt.figure(figsize=(16, 10))

# Bar chart
ax1 = plt.subplot(2, 2, 1)
bars = ax1.bar(main_metrics.keys(), main_metrics.values(), color=colors, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
ax1.set_title('Main Performance Metrics', fontsize=14, fontweight='bold', pad=20)
ax1.set_ylim([0, 100])
ax1.axhline(y=90, color='gray', linestyle='--', alpha=0.5)
ax1.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

# Comparison of averaging methods
ax2 = plt.subplot(2, 2, 2)
f1_scores = {
    'Micro': f1_micro * 100,
    'Macro': f1_macro * 100,
    'Weighted': f1_weighted * 100
}
colors2 = ['#9D4EDD', '#BD86FA', '#C77DFF']
bars2 = ax2.bar(f1_scores.keys(), f1_scores.values(), color=colors2, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('F1 Score (%)', fontsize=12, fontweight='bold')
ax2.set_title('F1 Score Comparison (Different Averages)', fontsize=14, fontweight='bold', pad=20)
ax2.set_ylim([0, 100])
ax2.grid(axis='y', alpha=0.3)

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

# Radar chart
ax3 = plt.subplot(2, 2, 3, projection='polar')
angles = np.linspace(0, 2 * np.pi, len(main_metrics), endpoint=False)
values = list(main_metrics.values())
values += values[:1]
angles = np.concatenate((angles, [angles[0]]))

ax3.plot(angles, values, 'o-', linewidth=2, color='#9D4EDD', label='DistilBERT')
ax3.fill(angles, values, alpha=0.25, color='#9D4EDD')
ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(main_metrics.keys(), fontsize=10)
ax3.set_ylim(0, 100)
ax3.set_title('Performance Radar Chart', fontsize=14, fontweight='bold', pad=20)
ax3.grid(True)
ax3.legend(loc='upper right')

# Summary table
ax4 = plt.subplot(2, 2, 4)
ax4.axis('tight')
ax4.axis('off')

table_data = [
    ['F1 Score (Micro)', f'{f1_micro*100:.2f}%'],
    ['F1 Score (Macro)', f'{f1_macro*100:.2f}%'],
    ['Accuracy', f'{accuracy*100:.2f}%'],
    ['Precision', f'{precision_micro*100:.2f}%'],
    ['Recall', f'{recall_micro*100:.2f}%'],
]

table = ax4.table(cellText=table_data,
                 colLabels=['Metric', 'Score'],
                 cellLoc='center',
                 loc='center',
                 colWidths=[0.6, 0.3])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

for i in range(2):
    table[(0, i)].set_facecolor('#9D4EDD')
    table[(0, i)].set_text_props(weight='bold', color='white')

for i in range(1, len(table_data) + 1):
    for j in range(2):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#F3EDFF')
        else:
            table[(i, j)].set_facecolor('#FAF7FF')
        table[(i, j)].set_edgecolor('black')

ax4.set_title('Detailed Performance Summary', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('./model/metrics_comprehensive.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Saved: metrics_comprehensive.png")

print("\n✅ All visualizations generated successfully!")
print("\nGenerated files:")
print("  - ./model/evaluation_results.txt")
print("  - ./model/metrics_presentation.png")
print("  - ./model/metrics_comprehensive.png")