# Description : This module contains the function to send email with the data as attachment


import configparser
from email.message import EmailMessage
import logging
import smtplib

## Variables
ConfigFile = "./Config/config.ini"
LogsFile = "./Logs/SupTrading.log"

## Logging configuration
logging.basicConfig(level=logging.INFO, filename=LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR, filename= LogsFile,
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


## function to read the email configuration file
def Config(filename=ConfigFile, section='Mailing'):
    Parser = configparser.ConfigParser()
    try:
        Parser.read(filename)
    except Exception as error:
        logger.error(f'{error}', exc_info=True)
        raise error
    email = {}
    if Parser.has_section(section):
        Params = Parser.items(section)
        for Param in Params:
            email[Param[0]] = Param[1]
        logger.info('Email config loaded')
    else:
        logger.error('Error in loading parameters')
        raise Exception(f'Section {section} not found in the {filename} file')
    return email

## function to send email with the data as attachment
def SendMail(To: list, Subject: str, Body: str, Attachment: str):
    try:
        Email = Config()
        Msg = EmailMessage()
        Msg['Subject'] = Subject
        Msg['From'] = Email['user']
        Msg['To'] = ", ".join(To)
        Msg.set_content(Body)
        with open(Attachment, 'rb') as File:
            Data = File.read()
            FileName = File.name
        Msg.add_attachment(Data, maintype='application', subtype='octet-stream', filename=FileName)
        logger.info('Sending email...')
        with smtplib.SMTP_SSL(Email['host'], Email['port']) as Server:
            Server.login(Email['user'], Email['password'])
            Server.send_message(Msg)
        logger.info('Email sent')
    except Exception as error:
        logger.error(f'{error}', exc_info=True)
        raise error


# if __name__ == '__main__':
#     SendMail(["saghiraghiles5032@gmail.com"], "Test", "Test", "./Data/cac40.csv")
#     logger.info('Ending main function')