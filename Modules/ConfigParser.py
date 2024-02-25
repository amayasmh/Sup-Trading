# Description: This module contains the configParser function


import configparser
import datetime
import logging


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


# Function to read the database configuration file
def Config(section):
    Parser = configparser.ConfigParser()
    try:
        Parser.read(ConfigFile)
    except Exception as error:
        logger.error(f'{error}', exc_info=True)
        raise error
    cf = {}
    if Parser.has_section(section):
        Params = Parser.items(section)
        for Param in Params:
            cf[Param[0]] = Param[1]
        logger.info('Parser config loaded')
    else:
        logger.error('Error in loading parameters')
        raise Exception(f'Section {section} not found in the {ConfigFile} file')
    return cf
