## Description: This module contains the scraping function for the SupTrading website


from bs4 import BeautifulSoup
import csv
from datetime import datetime
import logging
import os
import requests

## Variables
LogsFile = "./Logs/SupTrading.log"
DataFile = "./Data/cac40.csv"

logging.basicConfig(level=logging.INFO, filename=LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.ERROR, filename= LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

## Function to save data to a csv file with 
def SaveData(data: dict, filename: str):
    # Si le fichier n'existe pas, écrivez le header
    if not os.path.isfile(filename):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()

    # Écrire les données dans le fichier
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writerows(data)

## Scraping function for Boursorama website to get CAC40 data, returns a dictionary if successful
def SupTradingScraperCAC40(url: str, header: dict):
    logging.info("Starting scraper...")
    try:
        Response = requests.get(url, headers=header)
    except Exception as e:
        logging.error(f"Request failed: {e}")
        raise e
    logging.info("Request successful")
    Soup = BeautifulSoup(Response.content, "html.parser")
    logging.info("Parsing HTML...")
    CodeHtml = Soup.find('div', class_='c-faceplate c-faceplate--index is-positive /*debug*/')
    data = {}
    data["company"] = CodeHtml.find('a', class_='c-faceplate__company-link').text.strip()
    data["price"] = CodeHtml.find('span', class_='c-instrument c-instrument--last').text
    data["variation"] = CodeHtml.find('span', class_='c-instrument c-instrument--variation').text
    data['open'] = CodeHtml.find('span', class_='c-instrument c-instrument--open').text
    data['high'] = CodeHtml.find('span', class_='c-instrument c-instrument--high').text
    data['low'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text
    data['volume'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text
    data['tradeDate'] = CodeHtml.find('span', class_='c-instrument c-instrument--tradedate').text
    data['saveDate'] = datetime.today()
    logging.info("Scraper finished")
    return data


# if __name__ == "__main__":
#     Result = SupTradingScraperCAC40("https://www.boursorama.com/bourse/indices/cours/1rPCAC/", {})
#     print(Result)
#     SaveData([Result], DataFile)