import datetime
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep as wait
from Modules.ConfigParser import Config
from Modules.DatabaseFunctions import (Connect, Close, CreateAllTables, InsertDataCac40, InsertDataCompanies, InsertDataPerformance)
from Modules.DateTime import WaitUntil
from Modules.Scraping import (SupTradingScraperCAC40, SupTradingScraperCAC40Company, SaveDataCsv)
from Modules.SendMail import SendMail
# Variables
ConfigFile = "./Config/config.ini"
DataFile = "Data/SupTradingData_" + datetime.datetime.now().strftime("%Y%m%d") + ".csv"
UrlCac40 = "https://www.boursorama.com/bourse/indices/cours/1rPCAC/"  # CAC40 URL
# Logging configuration with name date and time
logging.basicConfig(level=logging.INFO, filename="Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.ERROR, filename="Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
def scrape_company_data(url, headers):
    return SupTradingScraperCAC40Company(url, headers)
def scrape_cac40_data(url, headers):
    return SupTradingScraperCAC40(url, headers)
# Main function to scrape data from Boursorama and save it to the database, send email and stop the program after 6pm and start again at 9am
if __name__ == "__main__":
    logger.info("Starting SupTrading main function")
    print("---------- Starting SupTrading main function ----------")
    Urls_companies = Config("CAC40_Companies_Urls")
    IterationTime = int(list(Config("Parameters").values())[0])
    Conn, Cur = Connect()
    CreateAllTables(Conn, Cur)
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                while datetime.datetime.now().weekday() < 5:
                    while (datetime.datetime.now().time() >= datetime.time(9, 0) and datetime.datetime.now().time() <= datetime.time(18, 5)):
                        start_time = time.time()
                        if Conn is None or Cur is None:
                            Conn, Cur = Connect()
                        company_tasks = [executor.submit(scrape_company_data, Urls_companies[company], {"User-Agent": "Mozilla/5.0"}) for company in Urls_companies]
                        cac40_task = executor.submit(scrape_cac40_data, UrlCac40, {"User-Agent": "Mozilla/5.0"})
                        for task in company_tasks:
                            InsertDataCompanies(Conn, Cur, task.result())
                        InsertDataCac40(Conn, Cur, cac40_task.result())
                        end_time = time.time()
                        print("------- Données collectées - Temps d'exécution de l'algorithme :", end_time - start_time, "secondes -------")
                        InsertDataPerformance(Conn, Cur, end_time - start_time)
                        wait(IterationTime * 60)
                    start_time = time.time()
                    logger.info("Sending email and stopping program until 9am next day")
                    company_data = [(company, scrape_company_data(Urls_companies[company], {"User-Agent": "Mozilla/5.0"})) for company in Urls_companies]
                    cac40_data = scrape_cac40_data(UrlCac40, {"User-Agent": "Mozilla/5.0"})
                    for company, data in company_data:
                        SaveDataCsv(data, DataFile)
                    SaveDataCsv(cac40_data, DataFile)
                    SendMail("SupTrading CAC40 OFF", "Hi,\n\nJust to inform you that the trading is off now. It will start again at 9am of the next working day.The last data is attached.\nBest regards,\n\nSupTradingBot", DataFile)
                    print("------- Email sent with data attached. Program stopped until 9am of the next working day -------")
                    try:
                        os.remove(DataFile)
                    except:
                        logger.error("Error while deleting Data file after sending email")
                        pass
                    end_time = time.time()
                    print("------- Data collected - Algorithm execution time:", end_time - start_time, "seconds -------")
                    InsertDataPerformance(Conn, Cur, end_time - start_time)
                    Close(Conn, Cur)
                    WaitUntil(9, 0)
                    logger.info("Starting main function again")
                logger.info("The program is off now. It will start again at 9am of the next working day")
                Close(Conn, Cur)
                WaitUntil(9, 0)
                logger.info("---------- Starting main function again ----------")
    except KeyboardInterrupt:
        logger.info("Program stopped by the user")
        print("#### SupTrading program stopped by the user ####")
        Close(Conn, Cur)
