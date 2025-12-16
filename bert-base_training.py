from datasets import load_dataset
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np
import torch
from sklearn.metrics import f1_score

# -------------------------------
# PyTorch 2.6 pickle fix
# -------------------------------
torch.serialization.add_safe_globals([
    np.ndarray,
    np._core.multiarray._reconstruct,
    torch.Generator
])

# -------------------------------
# 1️⃣ Dataset
# -------------------------------
dataset = load_dataset("go_emotions")
train = dataset["train"]
test = dataset["test"]

# -------------------------------
# 2️⃣ Tokenizer & Model (BERT-base)
# -------------------------------
num_labels = 28
checkpoint_path = "./results_bert/checkpoint-last"  # varsa resume

try:
    model = BertForSequenceClassification.from_pretrained(
        checkpoint_path,
        num_labels=num_labels,
        problem_type="multi_label_classification"
    )
    print(f"✅ Resuming from checkpoint: {checkpoint_path}")
except:
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=num_labels,
        problem_type="multi_label_classification"
    )
    print("⚙️ Starting fresh BERT-base training...")

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# -------------------------------
# 3️⃣ Tokenization
# -------------------------------
def tokenize(batch):
    encodings = tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

    labels = []
    for labs in batch["labels"]:
        row = [0.0] * num_labels
        for i in labs:
            row[i] = 1.0
        labels.append(row)

    encodings["labels"] = labels
    return encodings

train = train.map(tokenize, batched=True)
test = test.map(tokenize, batched=True)

train.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
test.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# -------------------------------
# 4️⃣ Metrics
# -------------------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    if isinstance(logits, tuple):
        logits = logits[0]

    probs = torch.sigmoid(torch.tensor(logits))
    preds = (probs > 0.5).int()

    f1 = f1_score(labels, preds, average="micro")
    acc = (preds == labels).float().mean().item()

    return {
        "accuracy": acc,
        "f1_micro": f1
    }

# -------------------------------
# 5️⃣ Trainer Override (float labels)
# -------------------------------
class FloatTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        if "labels" in inputs:
            inputs["labels"] = inputs["labels"].to(torch.float32)

        outputs = model(**inputs)
        loss = outputs.loss
        return (loss, outputs) if return_outputs else loss

# -------------------------------
# 6️⃣ Training Arguments (BERT için ayarlı)
# -------------------------------
training_args = TrainingArguments(
    output_dir="./results_bert",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,   # 🔴 BERT için KÜÇÜK
    per_device_eval_batch_size=2,
    num_train_epochs=2,
    weight_decay=0.01,
    logging_steps=100,
    save_strategy="epoch",
    save_total_limit=1,
    fp16=torch.cuda.is_available(),  # varsa hızlandır
    report_to="none"
)

# -------------------------------
# 7️⃣ Trainer
# -------------------------------
trainer = FloatTrainer(
    model=model,
    args=training_args,
    train_dataset=train,
    eval_dataset=test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# -------------------------------
# 8️⃣ Train
# -------------------------------
trainer.train(resume_from_checkpoint=checkpoint_path if "checkpoint" in checkpoint_path else None)

# -------------------------------
# 9️⃣ Save final model
# -------------------------------
trainer.save_model("./modelsequence")
tokenizer.save_pretrained("./modelsequence")

print("✅ BERT-base training completed and model saved to ./modelsequence")
