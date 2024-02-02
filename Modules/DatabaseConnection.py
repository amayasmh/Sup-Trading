# Description: This module contains functions to connect to database, execute sql query and close connection


import configparser
import psycopg2
import psycopg2.extras
import logging

ConfigFile = "./Config/config.ini"
LogsFile = "./Logs/SupTrading.log"

logging.basicConfig(level=logging.INFO, filename=LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.ERROR, filename= LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## function to read the database configuration file
def Config(filename=ConfigFile, section='Postgresql'):
    Parser = configparser.ConfigParser()
    try:
        Parser.read(ConfigFile)
    except Exception as error:
        logger.error(f'{error}', exc_info=True)
        raise error
    db = {}
    if Parser.has_section(section):
        Params = Parser.items(section)
        for Param in Params:
            db[Param[0]] = Param[1]
        logger.info('Database config loaded')
    else:
        logger.error('Error in loading parameters')
        raise Exception(f'Section {section} not found in the {filename} file')
    return db

## function to connect to the database with connection object as return 
def Connect():
    try:
        Params = Config()
        # print(params)
        logger.info('Connecting to the PostgreSQL database...')
        try:
            conn = psycopg2.connect(**Params)
            logger.info('Connected to the PostgreSQL database')
        except Exception as error:
            logger.error(f'Error while connecting to the database : {error}', exc_info=True)
            raise error
        # close the communication with the PostgreSQL
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{error}', exc_info=True)
        raise error
    
## function to close the database connection with connection object as input
def Close(Conn):
    if Conn is not None:
        try:
            Conn.close()
            logger.info('Database connection closed.')
        except Exception as error:
            logger.error(f'{error}', exc_info=True)
            return error
    else:
        logger.error('Error closing database connection : connection is None')
        return Exception('Error closing database connection : connection is None')
    
## function to execute the sql query with connection object and sql query as input, returns the result of the query if successful
def Execute(Conn, Sql):
    try:
        Cur = Conn.cursor()
        Conn.commit()
        Cur.execute(Sql)
        logger.info('SQL executed successfully')
        Result = Cur.fetchall()
        Cur.close()
        return Result
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{error}', exc_info=True)
        raise error


# if __name__ == '__main__':
#     logger.info('Starting main function')
#     Connection = Connect()
#     Query = 'SELECT version()'
#     print('PostgreSQL database version:')
#     print(Execute(Connection, Query))
#     Close(Connection)
