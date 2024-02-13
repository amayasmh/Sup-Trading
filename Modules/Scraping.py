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


## Function to save Data to a csv file with 
def SaveDataCsv(Data: dict, filename: str):
    # Si le fichier n'existe pas, écrivez le header
    if not os.path.isfile(filename):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Data[0].keys())
            writer.writeheader()
    # Écrire les données dans le fichier
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Data[0].keys())
        writer.writerows(Data)

## Scraping function for Boursorama website to get CAC40 Data, returns a dictionary if successful
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
    Data = {}
    try:
        Data["company"] = CodeHtml.find('a', class_='c-faceplate__company-link').text.strip()
    except Exception as e:
        logging.error(f"Error while parsing company: {e}")
        Data["company"] = None
    try:
        Data["price"] = CodeHtml.find('span', class_='c-instrument c-instrument--last').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing price: {e}")
        Data["price"] = None
    try:
        Data["variation"] = CodeHtml.find('span', class_='c-instrument c-instrument--variation').text.replace('%', '')
    except Exception as e:
        logging.error(f"Error while parsing variation: {e}")
        Data["variation"] = None
    try:
        Data['open'] = CodeHtml.find('span', class_='c-instrument c-instrument--open').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing open: {e}")
        Data['open'] = None
    try:
        Data['high'] = CodeHtml.find('span', class_='c-instrument c-instrument--high').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing high: {e}")
        Data['high'] = None
    try: 
        Data['low'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing low: {e}")
        Data['low'] = None
    try:
        Data['volume'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        Data['volume'] = None
    try:
        Data['tradeDate'] = CodeHtml.find('span', class_='c-instrument c-instrument--tradedate').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing tradeDate: {e}")
        Data['tradeDate'] = None

    # Data['saveDate'] = datetime.today()
    logging.info("Scraper finished")
    return Data

def SupTradingDayOffScraperCAC40(url: str, header: dict):
    logging.info("Starting scraper...")
    try:
        Response = requests.get(url, headers=header)
    except Exception as e:
        logging.error(f"Request failed: {e}")
        raise e
    logging.info("Request successful")
    Soup = BeautifulSoup(Response.content, "html.parser")
    logging.info("Parsing HTML...")
    CodeHtml = Soup.find('div', class_='c-faceplate c-faceplate--index is-negative /*debug*/')
    Data = {}
    try:
        Data["company"] = CodeHtml.find('a', class_='c-faceplate__company-link').text.strip()
    except Exception as e:
        logging.error(f"Error while parsing company: {e}")
        Data["company"] = None
    try:
        Data["price"] = CodeHtml.find('span', class_='c-instrument c-instrument--last').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing price: {e}")
        Data["price"] = None
    try:
        Data["variation"] = CodeHtml.find('span', class_='c-instrument c-instrument--variation').text.replace(' ', '').replace('%', '')
    except Exception as e:
        logging.error(f"Error while parsing variation: {e}")
        Data["variation"] = None
    try:
        Data['open'] = CodeHtml.find('span', class_='c-instrument c-instrument--open').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing open: {e}")
        Data['open'] = None
    try:
        Data['high'] = CodeHtml.find('span', class_='c-instrument c-instrument--high').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing high: {e}")
        Data['high'] = None
    try: 
        Data['low'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing low: {e}")
        Data['low'] = None
    try:
        Data['volume'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        Data['volume'] = None
    try:
        Data['tradeDate'] = CodeHtml.find('span', class_='c-instrument c-instrument--tradedate').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing tradeDate: {e}")
        Data['tradeDate'] = None

    # Data['saveDate'] = datetime.today()
    logging.info("Scraper finished")
    return Data
