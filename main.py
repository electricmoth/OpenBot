#!/usr/bin/env python3

# OpenBot - auto RSPV for a meetup.com event
# author: 0le4nder

import os
import logging
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

# Set up logging
logging.basicConfig(filename='openbot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to initialize the logger
def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


class Bot:
    def __init__(self, email, passwd, evt_url):
        self.email = email
        self.passwd = passwd
        self.evt_url = evt_url
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Firefox()
        return self

    def __exit__(self, exc_type, exc_val, exc_tracebk):
        if self.driver:
            self.driver.quit()

    def login(self):
        """login to meetup.com"""
        logging.info("[+] Logging in...")
        time.sleep(1)
        self.driver.get(login_url)
        time.sleep(3)
        email_field = self.driver.find_element(By.NAME, "email")
        passwd_field = self.driver.find_element(By.NAME, "current-password")
        email_field.send_keys(self.email)
        time.sleep(1)
        passwd_field.send_keys(self.passwd)
        passwd_field.send_keys(Keys.ENTER)

    def check_if_going(self):
        """check if "you're going" is on target event page"""
        # going_xpath = "/html/body/div[1]/div[2]/div[2]/div[2]/main/div[3]/div[2]/div/div[2]/ul/li[1]/div/a/div[2]/div[2]/div/div/span"
        going_xpath = "//span[contains(text(), 'going!')]"
        try:
            going = self.driver.find_element(By.XPATH, (going_xpath))
            logging.info("found.")
            return True
        except NoSuchElementException:
            logging.info("not found.")
        return False

    def rsvp(self):
        """RSVP to target event"""
        attend_btn_id = "attend-event-btn-e-1"
        self.driver.get(self.evt_url)
        logging.info("[*] Checking for existing RSVP... ")
        if self.check_if_going():
            logging.info("\n[*] You have already RSVPd to this event.")
            return

        logging.info("[+] RSPVing to event...")
        try:
            # click 1st "attend" button
            attend_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, attend_btn_id)))
            attend_btn.click()
            # click 'attend-irl-btn'
            attend_btn2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='attend-irl-btn']")))
            attend_btn2.click()
        except NoSuchElementException:
            logging.error(f"\n[-] Could not find target.")
        finally:
            self.driver.get(self.evt_url)
            logging.info("[*] Checking to confirm RSVP... ")
            if self.check_if_going():
                logging.info("\n[+] OpenBot RSVPd to event!")
            else:
                logging.error("\n[-] OpenBot could not RSVP to this event.")

def main():
    init_logger()
    with Bot(EMAIL, PASSWD, EVENT_URL) as bot:
        bot.login()
        time.sleep(3)
        bot.rsvp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.")
