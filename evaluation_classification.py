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
import pandas as pd

def generate_prompt(question):
    prompt = f"<s>[INST]You are an expect classifier to classify healthcare and non-healthcare related questions. Please classify wether this question : \"{question}\" is healthcare related or not. Only answer yes or no.[/INST]"
    return prompt

def search_answer(result):
    # split_list = result.split(" ")
    # print(split_list)
    if "yes" in result or "Yes" in result:
        return 1
    else:
        return 0

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
base_model = "/root/autodl-tmp/models/Llama-2-7b-chat-hf"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)

df = pd.read_csv("/root/autodl-tmp/dataset/testset/classification.csv")

true_labels = list(df["label"])
predicted_labels = []
for question in df["question"]:
    # label = classification_pred(pipe, question)
    # print(question)
    prompt = generate_prompt(question)

    result = pipe(prompt)
    
    result = result[0]['generated_text']
    index = result.rfind("[/INST]")
    result = result[index+7:]
    print(result)
    label = search_answer(result)
    predicted_labels.append(label)

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

print(predicted_labels)

print(true_labels)