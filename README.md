# Online Healthcare Chatbot

 This is the implementation of Online Healthcare Chatbot for Course ARIN7102 Project.

 ## Quick Start

- [Introduction](#intro)
- [Coding](#codes)
- [Demo](#demo)
- [Acknowledgement](#Acknowledgement)
  

## intro

## codes
### Llama-2 Fine-tuning

Firstly, downloading the pre-trained Llama-2-7B model from huggingface by running the following code. Please replace the token and local_dir by your own token and the path where you want save the model
```
python codes/fineTune/download.py
```


We fine-tune LLama-2-7B by c adaptation technique called LoRA based on the combination of public dataset and private dataset. 

```
python codes/fineTune/main.py --model=$MODEL_PATH --dataset_path=$DATASET_PATH --output_dir=$OUTPUT_DIR --batch_size=1
```

## demo

## Acknowledgement
