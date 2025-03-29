# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00EC4E9E731D825CC6F5FEAF5A0B603C940ADB1AAA36DE7742F54F99A194549002CAA3AA6C7EDB112F3900B54CE2EAE6F011DA1EC6528904AEC622B6A2CD7CE7FB94C53CCDD216FE78CE0539E2AEFF1E9F557AA88B61DD68880A39E65D09A4FC814CE1D9B3E65458E9BD04CA6FAA85816869159D7A6EFFB2CB1024DE237BC2AFD05B8F0A3552F58305C3A20F59BED171781A74A32F3E4DC802D05AD7EB6869E7CC86C4734D53EFA7C71E8C23B336B5275B780E8A8FD228D29A7CDDECDD9C792AA32E446967692FEDD19666D36DEDA1BFEB2C4902550CE2EEE8D8B37ADF992F77BE859608543B41C527E341EE59340C65F7B1054D3E9BE066F83817A9AFCF05420B3AA814AA86BFDD552F5DCF5215FE489BD9EA62E9535C819ED00FA8B9D0A5908BD51A225257F71046BA1182FFBFD023B510E7AC370713FC2175CCE37FA4B85CA1B998135E8D9793EE7CE54C879701516C1BE2D2852DC8572BB68371547CB107F1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
