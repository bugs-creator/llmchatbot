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

# based on question and history chat log to answer questions
def chatbot_answer(question, history: list=None,reference=None):
    # system_prompt = "You are a helpful, respectful and honest health acknowledge assistant.\n\n If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    system_prompt = "You are a helpful, respectful and honest health acknowledge assistant."

    input_ = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>"
    input_history=""
    if history is not None:
        for i, (meg, ans) in enumerate(history):
            
            input_ += meg + "[/INST]" + ans + "</s><s>[INST]"

    if reference is not None:
        input_+=f'Please answer the question "{question}" based on {reference}. [/INST]'
    else:
        input_ += question + "[/INST]"
    
    return input_