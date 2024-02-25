# Version: 1.0
# Project : SupTrading
# Description : Scraping CAC40 data from Boursorama website and save it to a database


import datetime
import logging
from Modules.ConfigParser import Config
from Modules.DatabaseFunctions import Connect, Close, Execute, CreateTableCac40, CreateTableCompanies
from Modules.DateTime import wait_until, wait_until_tomorrow
from Modules.Scraping import SupTradingScraperCAC40, SupTradingScraperCAC40Company, SaveDataCsv
from Modules.SendMail import SendMail
import os
from time import sleep as wait


# Variables
ConfigFile = "./Config/config.ini"
DataFile = "Data/cac40.csv"
UrlCac40 = "https://www.boursorama.com/bourse/indices/cours/1rPCAC/" # CAC40 URL


# Logging configuration with name date and time
logging.basicConfig(level=logging.INFO,
                    filename= "Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.ERROR,
                    filename= "Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Main function
if __name__ == '__main__':
    logger.info('Starting main function')
    Urls_companies = Config('CAC40_Companies_Urls')
    Parameters = list(Config('Parameters').values())
    IterationTime = Parameters[0]
    print(IterationTime)
    CreateTableCac40()
    CreateTableCompanies()
    while True:
        current_time = datetime.datetime.now().time()
        ## Check if the current time is between 9am and 6:05pm to save the data to the database
        if current_time >= datetime.time(9, 0) and current_time <= datetime.time(18, 5):
            for company in Urls_companies:
                DataCompany = SupTradingScraperCAC40Company(Urls_companies[company], {'User-Agent': 'Mozilla/5.0'})
                Conn = Connect()
                Sql = "INSERT INTO COMPANIES (company, sector, price, variation, open, high, low, downward_limit, upward_limit, last_dividend, last_dividend_date, volume, valuation, capital, estimated_yield_2024, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                Values = (DataCompany["company"], DataCompany["sector"], DataCompany["price"], DataCompany["variation"], DataCompany["open"], DataCompany["high"], DataCompany["low"], DataCompany["downward_limit"], DataCompany["upward_limit"], DataCompany["last_dividend"], DataCompany["last_dividend_date"], DataCompany["volume"], DataCompany["valuation"], DataCompany["capital"], DataCompany["estimated_yield_2024"], DataCompany["tradeDate"])
                Execute(Conn, Sql, Values)
                Close(Conn)
                print(DataCompany)
            ## Save the data to the database
            Data = SupTradingScraperCAC40(UrlCac40, {'User-Agent': 'Mozilla/5.0'})
            Conn = Connect()
            Sql = "INSERT INTO CAC40 (company, price, variation, open, high, low, volume, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            Values = ("CAC40", Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["volume"], Data["tradeDate"])
            Execute(Conn, Sql, Values)
            Close(Conn)
            print(Data)
            ## Wait for 60 seconds before the next iteration
            wait(IterationTime*60)
        ## Check if the current time is after 6:05pm to send an email and stop the program until 9am next day
        elif current_time > datetime.time(18, 5):
            logger.info('Sending email and stopping program until 9am next day')
            for company in Urls_companies:
                DataCompany = SupTradingScraperCAC40Company(Urls_companies[company], {'User-Agent': 'Mozilla/5.0'})
                print(DataCompany)
                SaveDataCsv(DataCompany, DataFile)
                continue
            Data = SupTradingScraperCAC40(UrlCac40, {'User-Agent': 'Mozilla/5.0'})
            print(Data)
            SaveDataCsv(Data, DataFile)
            SendMail("SupTrading CAC40 OFF", "Hi,\n\nJust to inform you that the program is off now. It will start again tomorrow at 9am.\n\nSupTradingBot", DataFile)
            ## Delete Data file csv if it exists
            try:
                os.remove(DataFile)
            except:
                logger.error('Error while deleting Data file after sending email')
                pass
            wait_until_tomorrow(9, 0)  # Wait until 9am next day
            logger.info('Starting main function again')
        else:
            ## Wait until 9am to start the program
            wait_until(9, 0)
            logger.info('Starting main function again')