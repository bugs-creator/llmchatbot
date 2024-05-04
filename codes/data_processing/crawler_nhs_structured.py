#%%
import time
import csv
import json
import pandas as pd
from pathlib import Path
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser()
parser.add_argument('--output_path',type=str,default='./data_structured/')
parser.add_argument('--is_demonstration',type=bool,default=False)
args = parser.parse_args()

def get_div():
    div_li = dict()
    divs = driver.find_elements(By.XPATH, '//*[@id="maincontent"]/div/div/article/ol/div')
    div_count = len(divs)
    print(div_count)

    for li_i in range(div_count):
        div_lis = driver.find_elements(By.XPATH, f'//*[@id="maincontent"]/div/div/article/ol/div[{li_i}]/div/ul/li')
        div_li_count = len(div_lis)
        div_li[li_i] = div_li_count
        # print(li_i, div_li_count)

    return div_li

# all together
def get_title_intro():
    intr_xpath = '//div/div//p'
    sctn_title = driver.title.split('-')[0].strip()
    try:
        sctn_intro = driver.find_element(By.XPATH, intr_xpath).text
    except:
        sctn_intro = None
    return sctn_title, sctn_intro

def get_title_intro():
    intr_xpath = '//div/div//p'
    sctn_title = driver.title.split('-')[0].strip()
    try:
        sctn_intro = driver.find_element(By.XPATH, intr_xpath).text
    except:
        sctn_intro = None
    return sctn_title, sctn_intro

def get_question_answer(tt, ito):
    sctn_xpath = '//main/article/div/div/section'
    titles_xpath = '//main/article/div/div/section/h2'
    sctns = driver.find_elements(By.XPATH, sctn_xpath)
    titles = driver.find_elements(By.XPATH, titles_xpath)

    ttl_dict = dict()
    ttl_index_list = list()
    for si in range(1, len(sctns) + 1):
        sctn_xa = f'//main/article/div/div/section[{si}]/h2'
        try:
            sctn_id = driver.find_element(By.XPATH, sctn_xa)
            ttl_dict[si] = sctn_id.text
            ttl_index_list.append(si)
            # print(si, sctn_id.text, sctn_id.get_attribute('id'))
        except:
            pass

    qas = list()
    qai_start = [tt, ito]
    for ti in ttl_index_list:
        qai = qai_start.copy()
        sctn_xb = f'//main/article/div/div/section[{ti}]'
        sctn_content = driver.find_element(By.XPATH, sctn_xb)
        qai.append(ttl_dict[ti])
        qai.append(sctn_content.text[len(ttl_dict[ti]) + 1:])
        qas.append(qai)
        # print(ti, ttl_dict[ti])
        # print(sctn_content.text[len(ttl_dict[ti]) + 1:])
    # print(qas)
    return qas

def click_link_all(div_idx, li_idx):
    time.sleep(0.2)
    cdtn_link_xpath = f'//main/div/div/article/ol/div[{div_idx}]/div/ul/li[{li_idx}]/a'
    cdtn_link = driver.find_element(By.XPATH, cdtn_link_xpath)
    driver.execute_script('arguments[0].click()', cdtn_link)
    time.sleep(0.2)
    print(driver.title)

    title, intro = get_title_intro()
    if intro:
        qas = get_question_answer(title, intro)
        new_row = qas.copy()
    else:
        new_row = None

    driver.back()
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.2)

    return new_row

def run_structured_crawler(outdir:str, div_li, is_demonstration: bool=False) -> str:
    # create outdir
    path = Path(outdir)
    path.mkdir(exist_ok=True)

    headers = ['title', 'introduction', 'question', 'answer']
    output_filepath = path / 'nhs_structured.csv'
    with open(output_filepath, 'w', newline='', encoding='utf-8') as file:
        wtr = csv.writer(file)
        wtr.writerow(headers)

        if is_demonstration:
            # test run
            # only crawl conditions for single letter
            div_id = 41
            li_total = div_li[div_id]
            print(li_total)
            for lii in range(1, div_li[div_id] + 1):
                print(div_id, lii, end='\t')
                nr = click_link_all(div_id, lii)
                if nr:
                    wtr.writerows(nr)
                else:
                    pass
        else:
            # full run
            for div_idx, li in div_li.items():
                if li == 0:
                    continue
                for li_idx in range(1, li + 1):
                    print(div_idx, li_idx, end='\t')
                    nr = click_link_all(div_idx, li_idx)
                    if nr:
                        wtr.writerows(nr)
                    else:
                        pass

    return output_filepath


def strip_qa(outdir, csv_file):
    df = pd.read_csv(csv_file, encoding='utf-8')

    # all title and intros without duplicates
    df_name_intro_duplicates = df[['question','answer']]
    df_name_intro = df_name_intro_duplicates.drop_duplicates()
    df_name_intro = df_name_intro.reset_index(drop=True)
    df_name_intro.to_csv(outdir / 'nhs_name_intro.csv', index=False)

    # all questions and answers without duplicates
    df_qa_duplicates = df.iloc[:, [2, 3]]
    df_qa = df_qa_duplicates.drop_duplicates()
    df_qa = df_qa.reset_index(drop=True)
    df_qa.to_csv(outdir / 'nhs_qa.csv', index=False)


def add_qa_to_json(outdir):
    df_qa = pd.read_csv(outdir / 'nhs_qa.csv', encoding='utf-8')
    
    rows_dict = list()
    for idx, row in df_qa.iterrows():
        rows_dict.append(row.to_dict())

    with open(outdir / 'nhs_qa.json', 'w', encoding='utf-8') as jf:
        json.dump(rows_dict, jf, indent=4)

if __name__ == "__main__":
    # crawler settings
    url = 'https://www.nhs.uk/conditions/'
    #outdir = './data_structured/'
    #is_demonstration = True
    outdir = args.output_path #outdir = './data_structured/'
    is_demonstration = args.is_demonstration #is_demonstration = True

    # init driver
    driver = webdriver.Chrome()
    driver.get(url)
    agree_button = driver.find_element(By.XPATH, '//*[@id="nhsuk-cookie-banner__link_accept_analytics"]')
    driver.execute_script('arguments[0].click()', agree_button)
    # agree_button.click()
    time.sleep(0.2)
    outdir = Path(outdir)
    
    # start crawling
    div_li = get_div() # get divs (sections by starting letter)
    output_filepath = run_structured_crawler(outdir, div_li, is_demonstration) # start crawling / write to output file

    # reformat for llm training
    strip_qa(outdir, output_filepath) # filter to question and answer
    add_qa_to_json(outdir) # dump json
    
    # python crawler_nhs_structured.py --is_demonstration True