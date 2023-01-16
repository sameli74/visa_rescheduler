# -*- coding: utf8 -*-

import time
import configparser
from datetime import datetime
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from login import login
from reschedule import get_date
from reschedule import get_available_date
from notify import gmail_send_message, push_notification

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SENDER = "soroush.ameli@gmail.com"
RECEIVERS = ["soroush.ameli@gmail.com", "rezapour92z@gmail.com"]
SUBJECT = "Action Required: US Visa Appointment Available!"

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

def embassy_dates():
    dates = get_date(driver, configs)[:5]
    if not dates:
        msg = "List is empty. Consider shutting down the poller if the issue persists"
        gmail_send_message(msg, SENDER,
                          RECEIVERS,
                          "US Visa Poller Detection",
                          SCOPES
        )
        print("The date list was empty. Poller might have been detected")
        # sys.exit(1)
    else:
        print_dates(dates)
    return dates



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
    while True:
        if retry_count > 6:
            break
        try:
            print(datetime.today())
            print(f"Retry count: {retry_count}")
            dates = embassy_dates()
            if not dates:
                time.sleep(configs["cooldown_time"])
                continue
            date, last_seen = get_available_date(dates, last_seen, configs["my_schedule_date"])
            print(f"New date: {date}")
            if date:
                push_notification(dates, SENDER,
                                  RECEIVERS,
                                  SUBJECT,
                                  SCOPES,
                                  )
            time.sleep(configs["retry_time"])

        except:
            retry_count += 1
            time.sleep(configs["exception_time"])

    print("crashed!")
    gmail_send_message("", SENDER,
                      RECEIVERS,
                      "Action Required: US VISA Poller Crashed",
                      SCOPES,
                      )
