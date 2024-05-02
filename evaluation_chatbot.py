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
import nltk
# from nltk.tokenize import sent_tokenize, word_tokenize 
# nltk.download('punkt')

def tokenize(sentence):
    sentence = sentence.replace("."," ").replace(","," ").replace("\""," ").replace("\'"," ").replace("?"," ")
    return sentence.split(" ")
def generate_prompt(question):
    question = f"{question}"
    # result = pipe(f"<s>[INST] {prompt} [/INST]")
    prompt = f"<s>[INST]{question}[/INST]"
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
base_model = "/root/autodl-tmp/llm_training_outputs_update_wonhs/checkpoint-44000"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)

df = pd.read_csv("/root/autodl-tmp/dataset/testset/chatbot.csv")

true_labels = list(df["answer"])
predicted_labels = []
n = 0
for question in df["question"]:
    # label = classification_pred(pipe, question)
    print(question)
    prompt = generate_prompt(question)

    result = pipe(prompt)
    
    result = result[0]['generated_text']
    index = result.rfind("[/INST]")
    result = result[index+7:]
    # print(result)
    # label = search_answer(result)
    predicted_labels.append(result)
    n += 1
    if n == 3:
        break

predicted_labels = [tokenize(i) for i in predicted_labels]
true_labels = [tokenize(i) for i in true_labels]

score_total = 0
for i in range(3):
    BLEUscore = nltk.translate.bleu_score.sentence_bleu([true_labels[i]], predicted_labels[i])
    print(BLEUscore)
    score_total += BLEUscore

print(score_total/3)
print(predicted_labels)

# 0.06804575746232461