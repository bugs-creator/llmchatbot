import xml.etree.ElementTree as ET
import os
import pandas as pd
import argparse
import glob

# parser for xml as the dataset is in xml format originally
def xml_parser(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    res = []
    ans = []
    questions = root.findall(".//Question")
    for question in questions:
        res.append(question.text)
    answers = root.findall(".//Answer")
    for answer in answers:
        ans.append(answer.text)
    return res,ans

# get all xml files under the given path
def get_all_files_path(directory):
    file_paths = []
    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)):
            xml_files = glob.glob(os.path.join(directory, folder, "*.xml"))
            file_paths.extend(xml_files)
        

    return file_paths

# parser for all questions and coresponding answers
def parser_all_questions(save_path: str, data_path: str):
    all_questions = []
    all_answers = []

    for file_path in get_all_files_path(data_path):
        print(file_path)
        res,ans = xml_parser(file_path)
        all_questions.extend(res)
        all_answers.extend(ans)

    # use dataframe to save
    df = pd.DataFrame({"question":all_questions,"answer":all_answers})
    df.to_csv(save_path, index=False)
    # return all_questions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str,default="./dataset/MedQuAD")
    parser.add_argument('--save_path', type=str,default="./dataset/MedQuAD.csv")
  
    args = parser.parse_args()
    save_path = args.save_path

    parser_all_questions(save_path, args.data_path)
  
