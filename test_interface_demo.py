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




history_messages = []

def message_and_history(input, history):
    history = history or []
    print(input)
    output = test_2(input, history)
    history.append((input, output))
    return history, history

def test_2(msg, history: list = None):
    if msg == "What is the weather today?":
        print("yes")
        output = "Sorry, this question is not healthcare related. Please ask me healthcare related questions."
        return output
    elif msg == "What is Covid-19?":
        return "Covid is a disease caused by a virus. It is a member of the coronavirus family. Covid-19 is a respiratory illness that can spread from person to person. It is not the same as the common cold or flu. Covid-19 is a serious disease that can cause severe illness. It can also cause death. Covid-19 spreads easily from person to person. It spreads through close contact with an infected person. It can also spread through droplets that are in the air. "
    elif msg == "What is its symptoms?":
        return "The symptoms of Covid-19 are similar to those of other respiratory viruses. They include:\na cough\na fever\na runny nose\na sore throat\nheadache\nmuscle or body aches\ntiredness\nSome people who get Covid-19 have no symptoms at all. Others may have mild symptoms and don't know they have it.\nThe symptoms of Covid-19 can appear anywhere from 2 to 14 days after you're infected.\nThe symptoms of Covid-19 can be different in children. Children may have a runny nose, sneezing, a cough, and a fever. They may also have stomach problems, such as diarrhea or vomiting."
    else:
        return "Sorry, I dont understand"


block = gr.Blocks(theme=gr.themes.Monochrome())
with block:
    gr.Markdown("""<h1><center>🤖️Healthcare Chatbot - Group3.1</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Hi, I am a healthcare Chatbot. May I help you?")
    state = gr.State()
    submit = gr.Button("Ask")
    submit.click(message_and_history,
          inputs=[message, state],
          outputs=[chatbot, state])
block.launch(share=True, debug=True)

