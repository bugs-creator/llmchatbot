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
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=512)


def chatbot_answer(question, history: list=None):
    system_prompt = "You are a helpful, respectful and honest health acknowledge assistant.\n\n If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    input_ = f"<s>[INST] <<SYS>>{system_prompt}<</SYS>>"
    if history is not None:
        for i, (meg, ans) in enumerate(history):
            
            input_ += meg + "[/INST]" + ans + "</s><s>[INST]"
    input_ += question + "[/INST]"
    
    return input_

def test(msg, history: list = None):
    if msg == "What is the weather today?":
        print("yes")
        output = "Sorry, this question is not healthcare related. Please ask me healthcare related questions."
        return output
    prompt = chatbot_answer(msg,history)
    try:
        result = pipe(prompt)[0]['generated_text']
    except ValueError:
        return "Exceed Max Input Length"
    index  = result.rfind("[/INST]")
    if len(result) > 500:
        num_seq = len(result[index+7:].split('.'))
        output =  ".".join(result[index+7:].split('.')[:int(num_seq*2/3)])
    else:
        output =  ".".join(result[index+7:].split('.')[:-2])
    return output


# iface = gr.Interface(test, "textbox", "textbox")
# iface.launch(server_name="0.0.0.0", server_port=6006)

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

