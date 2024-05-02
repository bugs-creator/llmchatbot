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
import argparse
import pandas as pd

# function to generate classification prompt
def generate_prompt(question):
    prompt = f"You are an expect classifier to classify healthcare and non-healthcare related questions. Please classify wether this question : \"{question}\" is healthcare related or not. Only answer yes or no."
    return prompt

# convert string answer to one-hot annotation (0 or 1), 0 for non-healthcare related question, 1 for healthcare related
def search_answer(result):
    split_list = result.split(" ")
    if "no" or "No" in split_list:
        return 0
    else:
        return 1

# based on llm model with input question to classify whether the input question is healthcare related or not
def classification_pred(pipe,question ):
    prompt = generate_prompt(question)
    result = pipe(question)[0]['generated_text']
    label = search_answer(result)
    return label

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str,required=True)
    parser.add_argument('--dataset_path',type=str,required=True)

    args = parser.parse_args()
    # set to float16
    compute_dtype = getattr(torch, "float16")

    # load basic config
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=False,
    )
    # model path
    base_model = args.model_path
    # load model
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=quant_config,
        device_map={"": 0}
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=128)

    # read the test data set
    df = pd.read_csv(args.dataset_path)

    # load ground truth label
    true_labels = list(df["label"])
    predicted_labels = []
    # for each question, let llm with prompt engineering to determine the label
    for question in df["question"]:
        label = classification_pred(pipe, question)
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

if __name__ == "__main__":
    main()


