# Description: This is the main file of the SupTrading project. It contains the main function to scrape data from Boursorama and save it to the database, send email and stop the program after 6pm and start again at 9am.
# Author: Aghiles, Amayas, Assia, Sarah
# Last updated: 2024-03-07
# Version: 1.0

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

# Configuration pour les messages d'information
info_logger = logging.getLogger(__name__ + "_INFO")
info_handler = logging.FileHandler("Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log")
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))  # Définir le format
info_logger.addHandler(info_handler)
info_logger.setLevel(logging.INFO)  # Définir le niveau de journalisation

# Configuration pour les messages d'erreur
error_logger = logging.getLogger(__name__ + "_ERROR")
error_handler = logging.FileHandler("Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log")
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))  # Définir le format
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)  # Définir le niveau de journalisation


def ScrapeCompanyData(url, headers):
    return SupTradingScraperCAC40Company(url, headers)
def scrape_cac40_data(url, headers):
    return SupTradingScraperCAC40(url, headers)

# Main function to scrape data from Boursorama and save it to the database, send email and stop the program after 6pm and start again at 9am
if __name__ == "__main__":
    try:
        info_logger.info("Starting SupTrading main function")
        print("---------- Starting SupTrading main function ----------")
        UrlsCompanies = Config("CAC40_Companies_Urls")
        IterationTime = int(list(Config("Parameters").values())[0])
        Conn, Cur = Connect()
        CreateAllTables(Conn, Cur)
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                while True:
                    while datetime.datetime.now().weekday() < 5:
                        while (datetime.datetime.now().time() >= datetime.time(9, 0) and datetime.datetime.now().time() <= datetime.time(18, 5)):
                            StartTime = time.time()
                            if Conn is None or Cur is None:
                                Conn, Cur = Connect()
                            CompanyTasks = [executor.submit(ScrapeCompanyData, UrlsCompanies[company], {"User-Agent": "Mozilla/5.0"}) for company in UrlsCompanies]
                            cac40_task = executor.submit(scrape_cac40_data, UrlCac40, {"User-Agent": "Mozilla/5.0"})
                            for task in CompanyTasks:
                                InsertDataCompanies(Conn, Cur, task.result())
                            InsertDataCac40(Conn, Cur, cac40_task.result())
                            EndTime = time.time()
                            print("------- Données collectées - Temps d'exécution de l'algorithme :", EndTime - StartTime, "secondes -------")
                            InsertDataPerformance(Conn, Cur, EndTime - StartTime)
                            wait(IterationTime * 60)
                        StartTime = time.time()
                        info_logger.info("Sending email and stopping program until 9am next day")
                        CompanyData = [(company, ScrapeCompanyData(UrlsCompanies[company], {"User-Agent": "Mozilla/5.0"})) for company in UrlsCompanies]
                        cac40_data = scrape_cac40_data(UrlCac40, {"User-Agent": "Mozilla/5.0"})
                        for company, data in CompanyData:
                            SaveDataCsv(data, DataFile)
                        SaveDataCsv(cac40_data, DataFile)
                        SendMail("SupTrading CAC40 OFF", "Hi,\n\nJust to inform you that the trading is off now. It will start again at 9am of the next working day.The last data is attached.\nBest regards,\n\nSupTradingBot", DataFile)
                        print("------- Email sent with data attached. Program stopped until 9am of the next working day -------")
                        try:
                            os.remove(DataFile)
                        except:
                            error_logger.error("Error while deleting Data file after sending email")
                            pass
                        EndTime = time.time()
                        print("------- Data collected - Algorithm execution time:", EndTime - StartTime, "seconds -------")
                        InsertDataPerformance(Conn, Cur, EndTime - StartTime)
                        Close(Conn, Cur)
                        WaitUntil(9, 0)
                        info_logger.info("Starting main function again")
                    info_logger.info("The program is off now. It will start again at 9am of the next working day")
                    Close(Conn, Cur)
                    WaitUntil(9, 0)
                    info_logger.info("---------- Starting main function again ----------")
        except KeyboardInterrupt:
            info_logger.info("Program stopped by the user")
            print("#### SupTrading program stopped by the user ####")
            Close(Conn, Cur)
    except Exception as e:
        SendMail("SupTrading ERROR", f"Hi,\n\nJust to inform you that the SupTrading program has stopped due to an error: {e}. Check the logs for more information.\nBest regards,\n\nSupTradingBot")
        error_logger.error(f"Error while executing SupTrading main function: {e}", exc_info=True)
        print("#### SupTrading program stopped due to an error ####")
        raise e