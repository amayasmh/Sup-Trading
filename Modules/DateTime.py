## Description: This module contains functions to wait until a specific time of the day or until a specific time of the next day.


import datetime
import time


## Wait until a specific time of the day
def wait_until(hour, minute):
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour, minute)
    if current_time < target_time:
        # Calculate the time difference until the target time
        time_difference = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.now()
        # Convert the time difference to seconds
        seconds_to_wait = time_difference.total_seconds()
        # Wait until the target time
        time.sleep(seconds_to_wait)

## Wait until a specific time of the next day
def wait_until_tomorrow(hour, minute):
    current_datetime = datetime.datetime.now()
    target_datetime = current_datetime.replace(hour=hour, minute=minute)
    if current_datetime > target_datetime:
        # Add one day to the target datetime
        target_datetime += datetime.timedelta(days=1)
    # Calculate the time difference until the target datetime
    time_difference = target_datetime - current_datetime
    # Convert the time difference to seconds
    seconds_to_wait = time_difference.total_seconds()
    # Wait until the target datetime
    time.sleep(seconds_to_wait)