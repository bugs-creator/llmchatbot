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

guanaco_dataset = "mlabonne/guanaco-llama2-1k"

dataset = load_dataset(guanaco_dataset, split="train")




pass