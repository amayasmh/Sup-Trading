from Modules.DatabaseConnection import Connect, Close, Execute
import logging

LogsFile = "Logs/SupTrading.log"

logging.basicConfig(level=logging.INFO, filename=LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.ERROR, filename= LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('Starting main function')
    Connection = Connect()
    Query = 'SELECT version()'
    print('PostgreSQL database version:')
    print(Execute(Connection, Query))
    Close(Connection)
