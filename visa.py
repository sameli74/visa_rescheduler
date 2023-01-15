# -*- coding: utf8 -*-

import time
# import platform
import configparser
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from login import login
from reschedule import get_date
from reschedule import get_available_date



# SENDGRID_API_KEY = config['SENDGRID']['SENDGRID_API_KEY']
# PUSH_TOKEN = config['PUSHOVER']['PUSH_TOKEN']
# PUSH_USER = config['PUSHOVER']['PUSH_USER']

# # def MY_CONDITION(month, day): return int(month) == 11 and int(day) >= 5
# def MY_CONDITION(month, day): return True # No custom condition wanted for the new scheduled date



def get_driver(configs):
    if configs.get("local_use", True):
        dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    else:
        dr = webdriver.Remote(command_executor=configs.get("hub_address", "http://localhost:9515/wd/hub"), options=webdriver.ChromeOptions())
    return dr

def print_dates(dates):
    print("Available dates:")
    for d in dates:
        print("%s \t business_day: %s" % (d.get('date'), d.get('business_day')))
    print()



if __name__ == "__main__":
    configs = configparser.ConfigParser()
    configs.read('config.ini')
    configs = dict(configs.items("USVISA"))
    configs["step_time"] = int(configs["step_time"])
    configs["exception_time"] = int(configs["exception_time"])
    configs["retry_time"] = int(configs["retry_time"])
    configs["cooldown_time"] = int(configs["cooldown_time"])
    driver = get_driver(configs)
    login(driver, configs)
    retry_count = 0
    last_seen = None
    EXIT = False
    while 1:
        if retry_count > 6:
            break
        try:
            print(datetime.today())
            print(f"Retry count: {retry_count}")

            dates = get_date(driver, configs)[:5]
            if not dates:
              msg = "List is empty"
              EXIT = True
              # send_notification(msg)
            print_dates(dates)
            date = get_available_date(dates, last_seen, configs["my_schedule_date"])
            print(f"New date: {date}")
            if date:
                print("doing some operation")
                # reschedule(date)
                # push_notification(dates)

            if(EXIT):
                print("------------------exit")
                break

            if not dates:
              msg = "List is empty"
              # send_notification(msg)
              time.sleep(configs["cooldown_time"])
            else:
              time.sleep(configs["retry_time"])

        except:
            retry_count += 1
            time.sleep(configs["exception_time"])

    if(not EXIT):
        print("crashed!")
        # send_notification("HELP! Crashed.")
