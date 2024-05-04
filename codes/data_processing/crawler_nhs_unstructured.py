import csv
import re
from pathlib import Path
from typing import Dict
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager, gets correct version directly

parser = argparse.ArgumentParser()
parser.add_argument('--output_path',type=str,default='./data_unstructured/')
parser.add_argument('--is_demonstration',type=bool,default=False)
args = parser.parse_args()

def gather_hrefs_in_url_xpath(driver, url: str, xpath:str, is_demonstration: bool) -> Dict[str,str]:
    # load url
    driver.get(url) 

    # get parent element + condition elements
    parent_element = driver.find_element(By.XPATH, xpath) # get exact element with links of interest
    link_elements = parent_element.find_elements(By.TAG_NAME, "a") # Find all the link elements within the parent element

    # only do 10 if is_demonstration
    if is_demonstration:
        link_elements = link_elements[:10]

    # extract hyperlink for each illness
    illnesses = {}
    for link_element in link_elements:
        href = link_element.get_attribute("href")
        if '#' not in href: # ignore fragment identifiers
            illnesses[link_element.text] = href

    # return dico
    return illnesses

# open an url, find an xpath and get all text embedded in it
def get_url_text_with_xpath(driver, url, xpath):
    
    driver.get(url) # open url
    wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    #element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    text_elements=driver.find_elements(By.XPATH, xpath) # get all matched instances
    text = "\n".join(element.text for element in text_elements) # join them
    return text # return it


def gather_contents_from_hrefs(driver, illnesses: Dict[str,str]):
    # get text from each condition link
    conditions = {}
    for title, url in illnesses.items():
        text = get_url_text_with_xpath(driver,url,'//article')
        conditions[title] = text

    # return
    return conditions

def save_conditions(outdir: str, conditions: Dict[str,str]) -> None:
    # create outdir
    path = Path(outdir)
    path.mkdir(exist_ok=True)

    # write each condition to CSV
    for title, contents in conditions.items():
        # build filepath
        cleaned_title = re.sub(r'[^\w\s\d]', '', title).replace(' ', '_').lower()
        filepath = path / (cleaned_title + '.csv')

        # write it
        print(filepath)
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([contents])

if __name__ == "__main__":
    # init driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # crawler settings
    url = 'https://www.nhs.uk/conditions/'
    xpath = '/html/body/div[2]/main/div/div/article/ol'
    outdir = args.output_path #outdir = './data_unstructured/'
    is_demonstration = args.is_demonstration #is_demonstration = True

    # do crawl
    condition_links: Dict[str,str] = gather_hrefs_in_url_xpath(driver, url, xpath, is_demonstration) # grab links
    condition_contents: Dict[str,str] = gather_contents_from_hrefs(driver, condition_links) # extract links
    save_conditions(outdir,condition_contents) # save unstructured contents

    # quit driver
    driver.quit()

    # python crawler_nhs_unstructured.py --is_demonstration True