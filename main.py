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
from dataset import llama_dataset


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,default="NousResearch/Llama-2-7b-chat-hf")
parser.add_argument('--dataset',type=str,default="mlabonne/guanaco-llama2-1k")
parser.add_argument('--dataset_path',type=str,default=None)
parser.add_argument('--output_dir',type=str,default="outputs")
args = parser.parse_args()


# Model from Hugging Face hub
base_model = args.model

# New instruction dataset
guanaco_dataset = args.dataset

# Fine-tuned model
new_model = args.output_dir
if args.dataset_path is None:
    dataset = load_dataset(guanaco_dataset, split="train")
else:
    dataset = llama_dataset.LlamaDataset(file=args.dataset_path)

compute_dtype = getattr(torch, "float16")

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

peft_params = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
)

training_params = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=25,
    logging_steps=25,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="tensorboard"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_params,
    dataset_text_field="text",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_params,
    packing=False,
)

trainer.model.save_pretrained(new_model)
trainer.tokenizer.save_pretrained(new_model)

from tensorboard import notebook
# log_dir = "/root/tf-logs/"
# notebook.start("--logdir {} --port 4000".format(log_dir))
