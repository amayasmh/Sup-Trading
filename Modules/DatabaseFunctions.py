# Description: This module contains functions to connect to database, execute sql query and close connection


import configparser
import logging
import psycopg2
import psycopg2.extras

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
            logger.error(f'Error while connecting to the database: {error}', exc_info=True)
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
        logger.error('Error closing database connection: connection is None')
        return Exception('Error closing database connection: connection is None')
    
## function to execute the sql query with connection object and sql query as input, returns true if successful
def Execute(Conn, Sql, Data=None):
    try:
        Cur = Conn.cursor()
        Cur.execute(Sql, Data)
        Conn.commit()
        logger.info('SQL executed successfully')
        # Result = Cur.fetchall()
        Cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'Error while executing query: {error}', exc_info=True)
        raise error

## function to create the tables in the database, executed only once at the beginning
def CreateTables():
    try:
        Connection = Connect()
        Query = '''DROP TABLE IF EXISTS CAC40;
        CREATE TABLE IF NOT EXISTS CAC40 (
            id SERIAL PRIMARY KEY,
            company VARCHAR(255) NOT NULL,
            price FLOAT NOT NULL,
            variation FLOAT NOT NULL,
            open FLOAT NOT NULL,
            high FLOAT NOT NULL,
            low FLOAT NOT NULL,
            volume FLOAT NOT NULL,
            trade_date TIMESTAMP NOT NULL,
            save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );'''
        Execute(Connection, Query)
        Close(Connection)
    except Exception as e:
        logging.error(f"Error while creating tables: {e}")
        raise e
        