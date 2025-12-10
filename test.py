from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, TrainingArguments, Trainer
import numpy as np
import torch

# PyTorch 2.6 pickle fix (tek gereken)
torch.serialization.add_safe_globals([
    np.ndarray,
    np._core.multiarray._reconstruct,
    torch.Generator
])

torch.serialization.add_safe_globals([torch.Generator])
torch.serialization.add_safe_globals([__import__('numpy')._core.multiarray._reconstruct])
from sklearn.metrics import f1_score

# 1️⃣ Dataset
dataset = load_dataset("go_emotions")
train = dataset["train"]
test = dataset["test"]

# 2️⃣ Tokenizer & Model (resume varsa oradan yükle)
num_labels = 28
checkpoint_path = "./results/checkpoint-10853"  # 🔁 son kaydedilen checkpoint
try:
    model = DistilBertForSequenceClassification.from_pretrained(
        checkpoint_path,
        num_labels=num_labels,
        problem_type="multi_label_classification"
    )
    print(f"✅ Resuming from checkpoint: {checkpoint_path}")
except:
    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=num_labels,
        problem_type="multi_label_classification"
    )
    print("⚙️ Starting fresh training...")

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# 3️⃣ Tokenization
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

# 4️⃣ Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    if isinstance(logits, tuple):
        logits = logits[0]
    probs = torch.sigmoid(torch.tensor(logits))
    preds = (probs > 0.5).int()
    f1 = f1_score(labels, preds, average="micro")
    acc = (preds == labels).float().mean().item()
    return {"accuracy": acc, "f1_micro": f1}

# 5️⃣ Trainer Override
class FloatTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        if "labels" in inputs:
            inputs["labels"] = inputs["labels"].to(torch.float32)
        outputs = model(**inputs)
        loss = outputs.get("loss") if isinstance(outputs, dict) else outputs[0]
        return (loss, outputs) if return_outputs else loss

# 6️⃣ Training Args (yer tasarrufu + devam)
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=2,         # 1 yerine 2 (veya 3) epoch daha
    weight_decay=0.01,
    logging_steps=100,
    save_strategy="epoch",      # 🔁 sadece epoch sonunda kaydet
    save_total_limit=1,         # 💾 sadece 1 checkpoint tut (disk dolmaz)
)

# 7️⃣ Trainer
trainer = FloatTrainer(
    model=model,
    args=training_args,
    train_dataset=train,
    eval_dataset=test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 8️⃣ Train (resume)
trainer.train(resume_from_checkpoint=checkpoint_path)

# 9️⃣ Save final model
trainer.save_model("./model")
tokenizer.save_pretrained("./model")
print("✅ Training completed and model saved.")
