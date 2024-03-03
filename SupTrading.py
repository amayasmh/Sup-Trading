# Version: 1.0
# Project : Sup'Trading
# Description : Scraping CAC40 data from Boursorama website and save it to a database


import datetime
import logging
from Modules.ConfigParser import Config
from Modules.DatabaseFunctions import Connect, Close, Execute, CreateTableCac40, CreateTableCompanies, InsertDataCac40, InsertDataCompanies
from Modules.DateTime import wait_until, wait_until_tomorrow
from Modules.Scraping import SupTradingScraperCAC40, SupTradingScraperCAC40Company, SaveDataCsv
from Modules.SendMail import SendMail
import os
from time import sleep as wait


# Variables
ConfigFile = "./Config/config.ini"
DataFile = "Data/SupTradingData_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
UrlCac40 = "https://www.boursorama.com/bourse/indices/cours/1rPCAC/" # CAC40 URL


# Logging configuration with name date and time
logging.basicConfig(level=logging.INFO,
                    filename= "Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.ERROR,
                    filename= "Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Main function to scrape data from Boursorama and save it to the database, send email and stop the program after 6pm and start again at 9am
if __name__ == '__main__':
    logger.info('Starting main function')
    Urls_companies = Config('CAC40_Companies_Urls')
    Parameters = list(Config('Parameters').values())
    IterationTime = int(Parameters[0])
    Conn, Cur = Connect()
    CreateTableCac40(Conn, Cur)
    CreateTableCompanies(Conn, Cur)
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= datetime.time(9, 0) and current_time <= datetime.time(18, 5):
            if Conn is None or Cur is None:
                Conn, Cur = Connect()
            for company in Urls_companies:
                InsertDataCompanies(Conn, Cur, SupTradingScraperCAC40Company(Urls_companies[company], {'User-Agent': 'Mozilla/5.0'}))
            InsertDataCac40(Conn, Cur, SupTradingScraperCAC40(UrlCac40, {'User-Agent': 'Mozilla/5.0'}))
            wait(IterationTime*60)
        elif current_time > datetime.time(18, 5):
            logger.info('Sending email and stopping program until 9am next day')
            for company in Urls_companies:
                Data = SupTradingScraperCAC40Company(Urls_companies[company], {'User-Agent': 'Mozilla/5.0'})
                print(Data)
                SaveDataCsv(Data, DataFile)
            Data = SupTradingScraperCAC40(UrlCac40, {'User-Agent': 'Mozilla/5.0'})
            print(Data)
            SaveDataCsv(Data, DataFile)
            SendMail("SupTrading CAC40 OFF", "Hi,\n\nJust to inform you that the program is off now. It will start again tomorrow at 9am.\nThe data is attached.\n\nSupTradingBot", DataFile)
            try:
                os.remove(DataFile)
            except:
                logger.error('Error while deleting Data file after sending email')
                pass
            Close(Conn, Cur)
            wait_until_tomorrow(9, 0)
            logger.info('Starting main function again')
        else:
            print('The program is off now. It will start again at 9am.')
            logger.info('The program is off now. It will start again at 9am.')
            Close(Conn, Cur)
            wait_until(9, 0)
            logger.info('Starting main function again')
