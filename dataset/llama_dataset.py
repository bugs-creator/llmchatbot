from torch.utils.data import Dataset
import csv

class LlamaDataset(Dataset):

    def __init__(self, file,
                 prompt="You are a helpful, respectful and honest health acknowledge assistant.\n\n If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."):
        with open(file,encoding='utf-8') as f:
            reader=csv.reader(f)
            text=[]
            self.data=[]
            for row in reader:
                text.append(row)
                self.data.append(f"<s>[INST] <<SYS>>\n{prompt}\n<</SYS>>\n"
                                 f"{row[0]} [/INST] {row[1]} </s>")


    def __len__(self):
        return self.data.__len__()

    def __getitem__(self, item):
        return self.data[item]










if __name__ == '__main__':
    dataset=LlamaDataset("C:\\Users\Wenrui Liu\Desktop\新建文件夹 (7)\\nhs_qa.csv")
    pass