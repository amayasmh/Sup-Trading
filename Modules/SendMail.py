# Description : This module contains the function to send email with the data as attachment


from Modules.ConfigParser import Config
import datetime
from email.message import EmailMessage
import logging
import smtplib

# Variables
ConfigFile = "./Config/config.ini"
LogsFile = "./Logs/SupTrading.log"


# Logging configuration
logging.basicConfig(level=logging.INFO,
                    filename= "./Logs/INFO_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.ERROR,
                    filename= "./Logs/ERROR_" + datetime.datetime.now().strftime("%Y%m%d") + ".log",
                    filemode="a", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Function to send email with the data as attachment
def SendMail(Subject: str, Body: str, Attachment: str):
    try:
        Email = Config('Mailing')
        Msg = EmailMessage()
        Msg['Subject'] = Subject
        Msg['From'] = Email['user']
        Msg['To'] = Email['to']  # Utilisez la liste des destinataires spécifiée dans la configuration
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
