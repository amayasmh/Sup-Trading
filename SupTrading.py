import logging
from Modules.DatabaseFunctions import Connect, Close, Execute, CreateTables
from Modules.Scraping import SupTradingScraperCAC40, SupTradingDayOffScraperCAC40, SaveDataCsv
from Modules.SendMail import SendMail
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
        
        ## If the company is None, it means that the trading is off
        if Data["company"] == None:
            Data = SupTradingDayOffScraperCAC40(UrlCac40, {})
            ## Send the data to the administator
            logger.info(f"Trading off on Boursorama's website: {Data}")
            ## Send an email to the administrator
            SaveDataCsv([Data], DataFile)
            SendMail(["aghiles.saghir@supdevinci-edu.fr"], "Trading CAC40 off today", "Hi!\nTrading off on Boursorama's website, there is no data to save, the last data is attached.\nSee you tomorrow !\n\nSupTradingBot", DataFile)
            ## Wait until 9h of the next day
            wait(60*60*15)  
        else:
            ## Save the data to the database
            Conn = Connect()
            Sql = "INSERT INTO CAC40 (company, price, variation, open, high, low, volume, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            Values = ("CAC40", Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["volume"], Data["tradeDate"])
            Execute(Conn, Sql, Values)
            Close(Conn)
            print(Data)
            ## Wait for 60 seconds before the next iteration
            wait(IterationTime*60)
    logger.info('Ending main function')
