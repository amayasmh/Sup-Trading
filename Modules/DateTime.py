## Description: This module contains functions to wait until a specific time of the day or until a specific time of the next day.


import datetime
import time


## Wait until a specific time of the day
import datetime
import time

def WaitUntil(hour, minute):
    current_datetime = datetime.datetime.now()
    target_datetime = current_datetime.replace(hour=hour, minute=minute)
    
    # Si l'heure cible est déjà passée aujourd'hui, ajustez-la pour demain
    if current_datetime > target_datetime:
        target_datetime += datetime.timedelta(days=1)
    
    # Calculez la différence de temps jusqu'à l'heure cible
    time_difference = target_datetime - current_datetime
    
    # Convertissez la différence de temps en secondes
    seconds_to_wait = time_difference.total_seconds()
    
    # Attendez jusqu'à l'heure cible
    time.sleep(seconds_to_wait)
