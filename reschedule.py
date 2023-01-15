import json
from datetime import datetime
from selenium.webdriver.common.by import By

from login import login
from login import is_logged_in

DATE_URL = "https://ais.usvisa-info.com/{}/niv/schedule/{}/appointment/days/{}.json?appointments[expedite]=false"

def get_date(driver, configs):
    "This function searches for available dates in the embassy's calendar"
    date_url = DATE_URL.format(configs["country_code"], configs["schedule_id"], configs["facility_id"])
    driver.get(date_url)

    if not is_logged_in(driver):
        login(driver, configs)
        return get_date(driver, configs)
    else:
        content = driver.find_element(By.TAG_NAME, 'pre').text
        date = json.loads(content)
        return date


def is_earlier(date, schedule_date):
    my_date = datetime.strptime(schedule_date, "%Y-%m-%d")
    new_date = datetime.strptime(date, "%Y-%m-%d")
    result = my_date > new_date
    print(f'Is {my_date} > {new_date}:\t{result}')
    return result


def get_available_date(dates, last_seen, schedule_date):
    print("Checking for an earlier date:")
    for d in dates:
        date = d.get('date')
        if is_earlier(date, schedule_date) and date != last_seen:
            _, month, day = date.split('-')
            last_seen = date
            return date, last_seen

# import requests
# TIME_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment/times/{FACILITY_ID}.json?date=%s&appointments[expedite]=false"
# APPOINTMENT_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment"

# def get_time(date):
#     time_url = TIME_URL % date
#     driver.get(time_url)
#     content = driver.find_element(By.TAG_NAME, 'pre').text
#     data = json.loads(content)
#     time = data.get("available_times")[-1]
#     print(f"Got time successfully! {date} {time}")
#     return time


# def reschedule(date):
#     global EXIT
#     print(f"Starting Reschedule ({date})")
#
#     time = get_time(date)
#     driver.get(APPOINTMENT_URL)
#
#     data = {
#         "utf8": driver.find_element(by=By.NAME, value='utf8').get_attribute('value'),
#         "authenticity_token": driver.find_element(by=By.NAME, value='authenticity_token').get_attribute('value'),
#         "confirmed_limit_message": driver.find_element(by=By.NAME, value='confirmed_limit_message').get_attribute('value'),
#         "use_consulate_appointment_capacity": driver.find_element(by=By.NAME, value='use_consulate_appointment_capacity').get_attribute('value'),
#         "appointments[consulate_appointment][facility_id]": FACILITY_ID,
#         "appointments[consulate_appointment][date]": date,
#         "appointments[consulate_appointment][time]": time,
#     }
#
#     headers = {
#         "User-Agent": driver.execute_script("return navigator.userAgent;"),
#         "Referer": APPOINTMENT_URL,
#         "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
#     }
#
#     r = requests.post(APPOINTMENT_URL, headers=headers, data=data)
#     if(r.text.find('Successfully Scheduled') != -1):
#         msg = f"Rescheduled Successfully! {date} {time}"
#         send_notification(msg)
#         EXIT = True
#     else:
#         msg = f"Reschedule Failed. {date} {time}"
#         send_notification(msg)
