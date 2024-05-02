import argparse
import glob
import os
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--medquad_path', type=str,default="./dataset/MedQuAD.csv")
    parser.add_argument('--mquad_path', type=str,default="./dataset/mquad-v1.csv")
    parser.add_argument('--nhs_path', type=str,default="./dataset/nhs_qa.csv")
    parser.add_argument('--save_path', type=str,default="./dataset/combined_data.csv")
  
    args = parser.parse_args()
    medquad_path = args.medquad_path
    mquad_path = args.mquad_path
    nhs_path = args.nhs_path
    save_path = args.save_path

    df_medquad = pd.read_csv(medquad_path)
    df_medquad = df_medquad.dropna()
    df_mquad = pd.read_csv(mquad_path)
    df_nhs = pd.read_csv(nhs_path)

    deleted_cols = list(df_mquad.columns) - ['question', 'answer']
    question = []
    question.extend(list(df_medquad['question']))
    
    question.extend(list(df_nhs['question']))
    question.extend(list(df_mquad['question']))
    answer = []
    answer.extend(list(df_medquad['answer']))
    answer.extend(list(df_nhs['answer']))
    answer.extend(list(df_mquad['answer']))
    print("extended")
    df  = pd.DataFrame({"question":question,"answer":answer})
    df.to_csv(save_path,index=False)

if __name__ == '__main__':
    main()
