import argparse

import gradio as gr

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
from utils import *
import json



parser = argparse.ArgumentParser()

parser.add_argument('--model_path',type=str,default="/root/autodl-tmp/llm_training_outputs_update_wonhs/checkpoint-44000")  # option that takes a value
parser.add_argument('--enable_classification',action='store_true')
parser.add_argument('--max_length',type=int,default=500)
parser.add_argument('--enable_retrieval',action='store_true')
parser.add_argument('--retrieval_data_path',type=str,default="../retrieval_model/search.py")
parser.add_argument('--enable_history',action='store_true')
args = parser.parse_args()


MODEL_PATH = "/root/autodl-tmp/llm_training_outputs_update_wonhs/checkpoint-44000"


compute_dtype = getattr(torch, "float16")
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)
base_model = MODEL_PATH
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=args.max_length)



def search(query):
    cmd=f'python ../retrieval_model/search.py --path="{args.retrieval_data_path}" --method=api --query="{query}"'
    result = json.loads(os.popen(cmd).read())
    if result["result"].__len__!=0:
        f=open(os.path.join(args.retrieval_data_path,"documents", result["result"][0][0]))
        return f.read()
    else:
        return ""



def test(msg, history: list = None):
    print(f"[user message: {msg}]")

    if args.enable_classification:
        classification_result = classification_pred(pipe,msg)

        if classification_result == 0:
            output = "Sorry, this question is not healthcare related. Please ask me healthcare related questions."
            return output
    
    reference=None
    if args.enable_retrieval:
        reference=search(msg)
        if reference.__len__()>=400:
            reference=reference[:400]

    if not args.enable_history:
        history=[]
    while history.__len__()!=0:

        prompt = chatbot_answer(msg, history,reference)
        print(f"[prompt: {prompt}]")
        try:
            result = pipe(prompt,temperature=0.7, top_p=0.9,do_sample=True)[0]['generated_text']
            break
        # if the user input a very long question, we will ask the user to re-input
        except ValueError:
            # return "Exceed Max Input Length, Please re-input your question"
            history.pop(0)
    else:
        prompt = chatbot_answer(msg, history, reference)
        print(f"[prompt: {prompt}]")
        try:
            result = pipe(prompt, temperature=0.7, top_p=0.9, do_sample=True)[0]['generated_text']
        # if the user input a very long question, we will ask the user to re-input
        except ValueError:
            return "Exceed Max Input Length, Please re-input your question"
    # post-processing for answer generated by chatbot
    index  = result.rfind("[/INST]")
    print(f"[result: {result}]")
    output = result[index+7:]
    # if len(result) > 500:
    #     num_seq = len(result[index+7:].split('.'))
    #     output =  ".".join(result[index+7:].split('.')[:int(num_seq*2/3)])
    # else:
    #     output =  ".".join(result[index+7:].split('.')[:-2])
    print(f"[output: {output}]")
    return output


history_messages = []

def message_and_history(input, history):
    history = history or []
    output = test(input, history)
    history.append((input, output))
    return history, history

block = gr.Blocks(theme=gr.themes.Monochrome())
with block:
    gr.Markdown("""<h1><center>🤖️Chat Bot</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Hi, I am a healthcare Chatbot. May I help you?")
    state = gr.State()
    submit = gr.Button("Ask")
    submit.click(message_and_history,
          inputs=[message, state],
          outputs=[chatbot, state])
block.launch(share=True, debug=True)

