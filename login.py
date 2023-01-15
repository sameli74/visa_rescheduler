import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

REGEX_CONTINUE = "//a[contains(text(),'Continuar')]"

def login(driver, configs):
    # Bypass reCAPTCHA
    driver.get(f"https://ais.usvisa-info.com/{configs['country_code']}/niv")
    time.sleep(configs["step_time"])
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(configs["step_time"])

    print("Login start...")
    href = driver.find_element(By.XPATH, '//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
    href.click()
    time.sleep(configs["step_time"])
    Wait(driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))

    print("\tclick bounce")
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(configs["step_time"])

    do_login_action(driver, configs)


def do_login_action(driver, configs):
    print("\tinput email")
    user = driver.find_element(By.ID, 'user_email')
    user.send_keys(configs["username"])
    time.sleep(random.randint(1, 3))

    print("\tinput pwd")
    pw = driver.find_element(By.ID, 'user_password')
    pw.send_keys(configs["password"])
    time.sleep(random.randint(1, 3))

    print("\tclick privacy")
    box = driver.find_element(By.CLASS_NAME, 'icheckbox')
    box .click()
    time.sleep(random.randint(1, 3))

    print("\tcommit")
    btn = driver.find_element(By.NAME, 'commit')
    btn.click()
    time.sleep(random.randint(1, 3))
    # Wait(driver, 60).until(
    #     EC.presence_of_element_located((By.XPATH, REGEX_CONTINUE)))
    print("\tlogin successful!")

def is_logged_in(driver):
    content = driver.page_source
    if(content.find("error") != -1):
        return False
    return True
