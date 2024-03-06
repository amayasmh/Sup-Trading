# Description: This module contains functions to connect to database, execute sql query and close connection


from Modules.ConfigParser import Config
import configparser
import datetime
import logging
import psycopg2
import psycopg2.extras


# Variables
ConfigFile = "./Config/config.ini"
Conn, Cur = None, None


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
        logger.info('Connecting to the PostgreSQL database...')
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{error}', exc_info=True)
        raise error
    try:
        Conn = psycopg2.connect(**Params)
        Cursor = Conn.cursor()
        logger.info('Connected to the PostgreSQL database')
    except Exception as error:
        logger.error(f'Error while connecting to the database: {error}', exc_info=True)
        raise error
    return Conn, Cursor
    
# Function to close the database connection with connection object as input
def Close(Conn, Cur):
    if Conn is not None:
        try:
            Cur.close()
            Conn.close()
            logger.info('Database connection closed.')
        except Exception as error:
            logger.error(f'{error}', exc_info=True)
    else:
        logger.error('Error closing database connection: connection is None')
    
# Function to execute the sql query with connection object and sql query as input, returns true if successful
def Execute(Conn, Cur, Sql, Data=None):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
        Cur.execute(Sql, Data)
        Conn.commit()
        logger.info('SQL executed successfully')
        # Result = Cur.fetchall()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'Error while executing query: {error}', exc_info=True)
        raise error

# Function to create the tables in the database, executed only once at the beginning
def CreateTableCac40(Conn, Cur):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
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
        Execute(Conn, Cur, Query)
    except Exception as e:
        logging.error(f"Error while creating tables: {e}")
        raise e

# Function to insert the data of the CAC40 in the database, executed every time the data is scraped
def InsertDataCac40(Conn, Cur, Data):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
        Sql = "INSERT INTO CAC40 (company, price, variation, open, high, low, volume, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        Values = ("CAC40", Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["volume"], Data["tradeDate"])
        Execute(Conn, Cur, Sql, Values)
    except Exception as e:
        logging.error(f"Error while inserting CAC40 data: {e}")
        raise e

# Function to create the tables in the database, executed only once at the beginning
def CreateTableCompanies(Conn, Cur):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
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
        Execute(Conn, Cur, Query)
    except Exception as e:
        logging.error(f"Error while creating tables: {e}")
        raise e
    
# Function to insert the data of the companies in the database, executed every time the data is scraped
def InsertDataCompanies(Conn, Cur, Data):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
        Sql = "INSERT INTO COMPANIES (company, sector, price, variation, open, high, low, downward_limit, upward_limit, last_dividend, last_dividend_date, volume, valuation, capital, estimated_yield_2024, trade_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        Values = (Data["company"], Data["sector"], Data["price"], Data["variation"], Data["open"], Data["high"], Data["low"], Data["downward_limit"], Data["upward_limit"], Data["last_dividend"], Data["last_dividend_date"], Data["volume"], Data["valuation"], Data["capital"], Data["estimated_yield_2024"], Data["tradeDate"])
        Execute(Conn, Cur, Sql, Values)
    except Exception as e:
        logging.error(f"Error while inserting company data: {e}")
        raise e
    
# Function to create the tables in the database, executed only once at the beginning
def CreateTablePerformance(Conn, Cur):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
        Query = '''
        CREATE TABLE IF NOT EXISTS Performances (
            id SERIAL PRIMARY KEY,
            execute_time FLOAT,
            save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );'''
        Execute(Conn, Cur, Query)
    except Exception as e:
        logging.error(f"Erreur lors de la création de la table : {e}")
        raise e
    
# Function to insert the data of the performance in the database, executed every time the data is scraped
def InsertDataPerformance(Conn, Cur, ExecutionTime):
    if Conn is None or Cur is None:
        Conn, Cur = Connect()
    try:
        Sql = "INSERT INTO Performances (execute_time) VALUES (%s)"
        Values = (ExecutionTime,)  # Utiliser un tuple avec une virgule pour une seule valeur
        Execute(Conn, Cur, Sql, Values)
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion des données de performance : {e}")
        raise e
    
# Function to create the tables in the database, executed only once at the beginning
def CreateAllTables(Conn, Cur):
    CreateTableCac40(Conn, Cur)
    CreateTableCompanies(Conn, Cur)
    CreateTablePerformance(Conn, Cur)