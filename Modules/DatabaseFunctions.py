# Description: This module contains functions to connect to database, execute sql query and close connection


from Modules.ConfigParser import Config
import configparser
import datetime
import logging
import psycopg2
import psycopg2.extras

# Variables
ConfigFile = "./Config/config.ini"


# Logging configuration
logging.basicConfig(level=logging.INFO,
                    filename= "./Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.ERROR,
                    filename= "./Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to connect to the database with connection object as return 
def Connect():
    try:
        Params = Config('Postgresql')
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
    
# Function to close the database connection with connection object as input
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
    
# Function to execute the sql query with connection object and sql query as input, returns true if successful
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

# Function to create the tables in the database, executed only once at the beginning
def CreateTableCac40():
    try:
        Connection = Connect()
        Query = '''
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
        
# Function to insert the data of the companies in the database, executed every time the data is scraped
def CreateTableCompanies():
    try:
        Connection = Connect()
        Query = '''
        CREATE TABLE IF NOT EXISTS COMPANIES (
            id SERIAL PRIMARY KEY,
            company VARCHAR(255) NOT NULL,
            sector VARCHAR(255) NOT NULL,
            price FLOAT NOT NULL,
            variation FLOAT NOT NULL,
            open FLOAT NOT NULL,
            high FLOAT NOT NULL,
            low FLOAT NOT NULL,
            downward_limit FLOAT,
            upward_limit FLOAT,
            last_dividend VARCHAR,
            last_dividend_date DATE,
            volume FLOAT NOT NULL,
            valuation FLOAT,
            capital FLOAT,
            estimated_yield_2024 VARCHAR,
            trade_date TIMESTAMP NOT NULL,
            save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );'''
        Execute(Connection, Query)
        Close(Connection)
    except Exception as e:
        logging.error(f"Error while creating tables: {e}")
        raise e