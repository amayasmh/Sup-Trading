import logging
from Modules.DatabaseFunctions import Connect, Close, Execute, CreateTables
from Modules.Scraping import SupTradingScraperCAC40, SaveDataCsv


## Variables
LogsFile = "Logs/SupTrading.log"
DataFile = "./Data/cac40.csv"
UrlCac40 = "https://www.boursorama.com/bourse/indices/cours/1rPCAC/"

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
    Data = SupTradingScraperCAC40(UrlCac40, {})
    ## Save the data to the database
    Conn = Connect()
    Sql = "INSERT INTO CAC40 (company, price, variation, open, high, low, volume, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    Values = ("CAC40", Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["volume"], Data["tradeDate"])
    Execute(Conn, Sql, Values)
    Close(Conn)
    print(Data)
    SaveDataCsv([Data], DataFile)
