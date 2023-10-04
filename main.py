#!/usr/bin/env python3

# OpenBot - auto RSPV for a meetup.com event
# author: 0le4nder

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# ENVIRONMENT VARIABLES
EMAIL = os.getenv("EMAIL")
PASSWD = os.getenv("PASSWD")
EVENT_URL = os.getenv("EVENT_URL")

login_url = "https://www.meetup.com/login/"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, timeout=2)

class Bot:
    def __init__(self, email, passwd, evt_url):
        self.email = email
        self.passwd = passwd
        self.evt_url = evt_url

    def login(self):
        """login to meetup.com"""
        print("[+] Logging in...")
        time.sleep(1)
        driver.get(login_url)
        time.sleep(3)
        email_field = driver.find_element(By.NAME, "email")
        passwd_field = driver.find_element(By.NAME, "current-password")
        email_field.send_keys(self.email)
        time.sleep(1)
        passwd_field.send_keys(self.passwd)
        passwd_field.send_keys(Keys.ENTER)

    def check_if_going(self):
        """check if "you're going" is on target event page"""
        going_xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/main/div[3]/div[2]/div/div[2]/ul/li[1]/div/a/div[2]/div[2]/div/div/span"
        try:
            going = driver.find_element(By.XPATH, (going_xpath))
            text = going.get_attribute('innerHTML')
            if "going!" in text:
                print("found.")
                return True
        except Exception as e:
            print("not found.")
        return False

    def rsvp(self):
        """RSVP to target event"""
        attend_btn_id = "attend-event-btn-e-1"
        driver.get(self.evt_url)
        print("[*] Checking for existing RSVP... ", end="")
        if self.check_if_going():
            print("\n[*] You have already RSVPd to this event.")
            return
        try:
            print("[+] RSPVing to event...")
            # click 1st "attend" button
            attend_btn = wait.until(EC.element_to_be_clickable((By.ID, attend_btn_id)))
            attend_btn.click()
            # click 'attend-irl-btn'
            attend_btn2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='attend-irl-btn']")))
            attend_btn2.click()
        except Exception as e:
            print(f"\n[-] Could not find target.")
        finally:
            driver.get(self.evt_url)
            print("[*] Checking to confirm RSVP... ", end="")
            if self.check_if_going():
                print("\n[+] OpenBot RSVPd to event!")
            else:
                print("\n[-] OpenBot could not RSVP to this event.")

def main():
    bot = Bot(EMAIL, PASSWD, EVENT_URL)
    bot.login()
    time.sleep(3)
    bot.rsvp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.")
