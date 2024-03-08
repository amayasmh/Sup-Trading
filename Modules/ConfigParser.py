# Description: This module contains the configParser function


import configparser
import datetime
import logging


# Variables
ConfigFile = "./Config/config.ini"


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

# Function to read the database configuration file
def Config(section):
    Parser = configparser.ConfigParser()
    try:
        Parser.read(ConfigFile)
    except Exception as error:
        error_logger.error(f'{error}', exc_info=True)
        raise error
    cf = {}
    if Parser.has_section(section):
        Params = Parser.items(section)
        for Param in Params:
            cf[Param[0]] = Param[1]
        info_logger.info('Parser config loaded')
    else:
        error_logger.error('Error in loading parameters')
        raise Exception(f'Section {section} not found in the {ConfigFile} file')
    return cf
