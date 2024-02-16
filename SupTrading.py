## Version: 1.0
## Project : SupTrading
## Description : Scraping CAC40 data from Boursorama website and save it to a database


import datetime
import logging
from Modules.DatabaseFunctions import Connect, Close, Execute, CreateTables
from Modules.DateTime import wait_until, wait_until_tomorrow
from Modules.Scraping import SupTradingScraperCAC40, SaveDataCsv
from Modules.SendMail import SendMail
import os
from time import sleep as wait


## Variables
DataFile = "./Data/cac40.csv"
LogsFile = "Logs/SupTrading.log"
UrlCac40 = "https://www.boursorama.com/bourse/indices/cours/1rPCAC/" # CAC40 URL
IterationTime = 1 # in minutes

## Logging configuration
logging.basicConfig(level=logging.INFO, filename=LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR, filename= LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## Main function
if __name__ == '__main__':
    logger.info('Starting main function')
    # CreateTables() # Uncomment this line to create the table only once
    while True:
        Data = SupTradingScraperCAC40(UrlCac40, {})
        current_time = datetime.datetime.now().time()
        if current_time >= datetime.time(9, 0) and current_time <= datetime.time(18, 5):
            ## Save the data to the database
            Conn = Connect()
            Sql = "INSERT INTO CAC40 (company, price, variation, open, high, low, volume, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            Values = ("CAC40", Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["volume"], Data["tradeDate"])
            Execute(Conn, Sql, Values)
            Close(Conn)
            print(Data)
            ## Wait for 60 seconds before the next iteration
            wait(IterationTime*60)
        elif current_time > datetime.time(18, 5):
            ## Send email and stop program until 9am next day
            logger.info('Sending email and stopping program until 9am next day')
            print(Data.keys())
            SaveDataCsv(Data, DataFile)
            SendMail(["aghiles.saghir@supdevinci-edu.fr"], "SupTrading CAC40 OFF", "Hi,\n\nJust to inform you that the program is off now. It will start again tomorrow at 9am.\n\nSupTradingBot", DataFile)
            ## delete Data file if it exists
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
            
