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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E8626CEBDCD747F574A9B23C2F24719C77F02A49BD7AD8A36DF475B7190E6481D212A34376A973E95E772B4AC39A6F439F02B20C9CFFC3BD1F288F22B7EF9C1A6CC2612379CDBCAA5A79A961A21684ABFFF6E9440F3166EFCE1ED61728494B7BB8194030786D329F922EEBFC37D9315D7F24D458CD1FB6CC49E26B1367A35A269068281B369D8E233A519800A20228EFC6BFF9A162DB3109F4D64825E199CFA1C427893726C7759E2A192CDD3AD94A57F4CB988C84685BC7F27BCBFC56AAF9AD5957E073D515866C1BB7005F23ED21BE049C52C1C22FA1CFE0E10F833A21544304BC386BF7345A23534D2D1C49D525953AD6386791020F4E18706FA79D7E1EAB0DD3E559B03F7950570C2D88A8A21A7C1F34DF4C27F474D31E7C442A3EA7CDD0D84DE9DC1EAF3F58942E0FD92345D3BB88575D8A45B6D93CAED659C673DA0C6F113256F1812DB1F4ED71824135139D4C05BB8E50A848307EBFF1F1701A8F341B"})
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
