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
    browser.add_cookie({"name": "MUSIC_U", "value": "008424DC64F955A5D79FFCA5B60D09CD274CC86939F816008A60AF06318E1EE7439887EDE9DB72D9B94EA19B0B0DC6757DDC5988BE0F5B314E14D7FB6595FEBF116BEDB7DB2671D7DDB6D7D5B7492420797AFA5EE3AB4F38CCCC968CAABEF9FA6439C029D2B035558B84264D0D6E7297ECE9D7B43F68C2D552A7D660751895A1266B2681AE73F06129B773EB7C8DDB2B9EEA1C7C944C983CF0AE79AD53E3A0233583B1DEB5579FC2BFE760F616C13752B4F5907B8A3F307E90F8C179599BA6D8605C68A9DFC31DFA34AC8E3F85D4219A0C3E3304EF56A3E4FC3FBC407C0BFC799157B9EAA79BCEBD25FA356791F3CBEACAC739F007869EF05C7E97C24E1FB7048347BF727E0952C52017259FABB95196BC8D09A860D2380B7DEC98E6A9BC85ED99DB55E9E4DF1F39B1EC22E692B82646238689B0C95B1DA6D883513BCDF3E1A44C53DF8281BEAF7156A76803DCB4350F9268C8987A7DB29570E61223A3FDE6BD1E"})
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
