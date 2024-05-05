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

### Information Retreival Model

The dataset is available here (add the link to the data). Please download it and put it under the retrieval_model file.

When you first run this program, this will automatically generate ```corpus.json```, which contains the indexing result. When you run this program again, it will read this file, unless you delete this file.

You can use the below command to enter queries by hand:

```shell
python search.py -m manual
```

You can use the below command to evaluation:

```shell
python search.py -m evaluation
```

After it complete, it will generate ```output.txt```.

You can use the below command to connect to the large language model:

```shell
python search.py -m api
```

### Dataset Retrieval
Both versions of our NHS condition scrapers are listed here

Unstructured: the following extracts all article information form all listed conditions (fast run-time):
```shell
python crawler_nhs_unstructured.py
```

Structured: the following improves upon the above by pulling the results in a "question" and "answer" format which is better for LLM training (slower run-time):
```shell
python crawler_nhs_structured.py
```

In both cases, a ```--is_demonstration True``` flag runs a subset of the conditions for testing purposes, i.e.

```shell
python crawler_nhs_unstructured.py --is_demonstration True
python crawler_nhs_structured.py --is_demonstration True
```


## demo

You can run the chatbot with GUI in `code/fineTuning` with:

```shell
python user_interface.py \
--
```


## Acknowledgement
