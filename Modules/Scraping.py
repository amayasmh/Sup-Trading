## Description: This module contains the scraping function for the SupTrading website


from bs4 import BeautifulSoup
import csv
import datetime
import logging
import os
import requests


## Logging configuration
logging.basicConfig(level=logging.INFO,
                    filename= "./Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.ERROR,
                    filename= "./Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## Function to save Data to a csv file with 
def SaveDataCsv(Data: dict, filename: str):
    if not Data:
        logging.error("Data is empty, cannot save to CSV.")
        return
    # Verify if the Data is in the expected format
    if not isinstance(Data, dict):
        logging.error("Data is not in the expected format. Expected dictionary.")
        return
    # if the file does not exist, create it and write the header
    if not os.path.isfile(filename):
        with open(filename, 'a', newline='') as csvfile:
            try:
                writer = csv.DictWriter(csvfile, fieldnames=Data.keys())
                writer.writeheader()
                logging.info(f"File {filename} created")
            except Exception as e:
                logging.error(f"Error while creating csv: {e}")
                raise e
    # Write the data to the file
    with open(filename, 'a', newline='') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, fieldnames=Data.keys())
            writer.writerow(Data)  ## Utilisez writerow() pour écrire une seule ligne
            logging.info(f"Data written to {filename}")
        except Exception as e:
            logging.error(f"Error while writing to csv: {e}")
            raise e

## Scraping function for Boursorama website to get CAC40 Data, returns a dictionary if successful
def SupTradingScraperCAC40(url: str, header: dict):
    logging.info("Starting CAC40 scraper...")
    try:
        Response = requests.get(url, headers=header)
    except Exception as e:
        logging.error(f"Request failed: {e}")
        raise e
    logging.info("Request successful")
    Soup = BeautifulSoup(Response.content, "html.parser")
    logging.info("Parsing HTML...")
    CodeHtml = Soup.find('div', class_='c-faceplate c-faceplate--index is-positive /*debug*/')
    if CodeHtml is None:
        logging.info(f"Trading is negative")
        CodeHtml = Soup.find('div', class_='c-faceplate c-faceplate--index is-negative /*debug*/')
    else:
        logging.info(f"Trading is positive")
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
        Data['low'] = CodeHtml.find_all('span', class_='c-instrument c-instrument--low')[0].text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing low: {e}")
        Data['low'] = None
    try:
        Data['volume'] = int(CodeHtml.find_all('span', class_='c-instrument c-instrument--low')[1].text.replace(' ', '').replace('M€', '')) * 1000000
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        Data['volume'] = None
    try:
        Data['tradeDate'] = CodeHtml.find('span', class_='c-instrument c-instrument--tradedate').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing tradeDate: {e}")
        Data['tradeDate'] = None
    logging.info("CAC40 Scraper finished")
    return Data

## Scraping function for Boursorama website to get CAC40 companies's Data, returns a dictionary if successful
def SupTradingScraperCAC40Company(url: str, header: dict):
    logging.info("Starting company's scraper...")
    try:
        Response = requests.get(url, headers=header)
    except Exception as e:
        logging.error(f"Request failed: {e}")
        raise e
    logging.info("Request successful")
    Soup = BeautifulSoup(Response.content, "html.parser")
    logging.info("Parsing HTML...")
    CodeHtml = Soup.find('div', class_='c-faceplate is-positive /*debug*/')
    if CodeHtml is None:
        logging.info(f"Trading is negative")
        CodeHtml = Soup.find('div', class_='c-faceplate is-negative /*debug*/')
    else:
        logging.info(f"Trading is positive")
    DataCompany = {}
    try:
        DataCompany["company"] = CodeHtml.find('a', class_='c-faceplate__company-link').text.strip()
    except Exception as e:
        logging.error(f"Error while parsing company: {e}")
        DataCompany["company"] = None
    try:
        CodeHtmlTmp = CodeHtml.find('li', class_='c-list-info__item')
        DataCompany["sector"] = CodeHtmlTmp.find('p', class_='c-list-info__value u-color-big-stone').text.strip()
    except Exception as e:
        logging.error(f"Error while parsing sector: {e}")
        DataCompany["sector"] = None
    try:
        DataCompany["price"] = CodeHtml.find('span', class_='c-instrument c-instrument--last').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing price: {e}")
        DataCompany["price"] = None
    try:
        DataCompany["variation"] = CodeHtml.find('span', class_='c-instrument c-instrument--variation').text.replace('%', '')
    except Exception as e:
        logging.error(f"Error while parsing variation: {e}")
        DataCompany["variation"] = None
    try:
        DataCompany['open'] = CodeHtml.find('span', class_='c-instrument c-instrument--open').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing open: {e}")
        DataCompany['open'] = None
    try:
        DataCompany['high'] = CodeHtml.find('span', class_='c-instrument c-instrument--high').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing high: {e}")
        DataCompany['high'] = None
    try: 
        DataCompany['low'] = CodeHtml.find('span', class_='c-instrument c-instrument--low').text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing low: {e}")
        DataCompany['low'] = None
    try:
        CodeHtmlTmp = CodeHtml.find('div', class_='c-faceplate__data')
        DataCompany["downward_limit"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[8].text.replace(' ', '').replace('\n', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['downward_limit'] = None
    try:
        DataCompany["upward_limit"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[9].text.replace(' ', '').replace('\n', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['upward_limit'] = None
    try:
        DataCompany["last_dividend"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[12].text.replace(' ', '').replace('\n', '').replace('EUR', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['last_dividend'] = None
    try:
        DataCompany["last_dividend_date"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[13].text.replace(' ', '').replace('\n', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['last_dividend_date'] = None
    try:
        DataCompany["volume"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[4].text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['volume'] = None
    try:
        DataCompany["valuation"] = int(CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[6].text.replace(' ', '').replace('\n', '').replace('MEUR', '')) * 1000000
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['valuation'] = None
    try:
        DataCompany["capital"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[5].text.replace(' ', '').replace('\n', '').replace('%', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['capital'] = None
    try:
        DataCompany["estimated_yield_2024"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[10].text.replace(' ', '').replace('\n', '').replace('%', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['estimated_yield_2024'] = None
    try:
        DataCompany["tradeDate"] = CodeHtmlTmp.find_all('p', class_='c-list-info__value u-color-big-stone')[7].text.replace(' ', '')
    except Exception as e:
        logging.error(f"Error while parsing volume: {e}")
        DataCompany['tradeDate'] = None
    logging.info("Company's scraper finished")
    return DataCompany
