# Description : This module contains the function to send email with the data as attachment


from Modules.ConfigParser import Config
import datetime
from email.message import EmailMessage
import logging
import smtplib

# Variables
ConfigFile = "./Config/config.ini"
LogsFile = "./Logs/SupTrading.log"

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
        info_logger.info('Sending email...')
        with smtplib.SMTP_SSL(Email['host'], Email['port']) as Server:
            Server.login(Email['user'], Email['password'])
            Server.send_message(Msg)
        info_logger.info('Email sent')
    except Exception as error:
        error_logger.error(f'{error}', exc_info=True)
        raise error
