import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig
from trl import SFTTrainer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def generate_prompt(question):
    prompt = f"You are an expect classifier to classify healthcare and non-healthcare related questions. Please classify wether this question : \"{question}\" is healthcare related or not. Only answer yes or no."
    return prompt

def search_answer(result):
    split_list = result.split(" ")
    if "no" or "No" in split_list:
        return 0
    else:
        return 1

def classification_pred(pipe,question ):
    prompt = generate_prompt(question)
    result = pipe(question)[0]['generated_text']
    label = search_answer(result)
    return label

compute_dtype = getattr(torch, "float16")
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)
base_model = "/root/autodl-tmp/llm_training_outputs_update/checkpoint-1000"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=128)

df = pd.read_csv("/root/autodl-tmp/dataset/testset/classification.csv")

true_labels = list(df["label"])
predicted_labels = []
for question in df["question"]:
    label = classification_pred(pipe, question)
    pred_label.append(label)

# Calculate accuracy
accuracy = accuracy_score(true_labels, predicted_labels)
print("Accuracy:", accuracy)

# Calculate precision
precision = precision_score(true_labels, predicted_labels)
print("Precision:", precision)

# Calculate recall
recall = recall_score(true_labels, predicted_labels)
print("Recall:", recall)

# Calculate F1 score
f1 = f1_score(true_labels, predicted_labels)
print("F1 Score:", f1)


