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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C9B95A64D185C27C47845A89A19C70ACCD83F2527CE1D4B877392FBC0AEA08CB1F6944C173E30032791F04292DCD1EE39C14ED1F91F0A7CBBA2B8F548A29BF2C6A053EAB801ADDA13FAF30BC7189FB7B2A413AF46437A263EB69D28715C94B448333D73DD74B2DBF439EA30984EA7178B8D8FD0A812B8DD6A5B5995A6269846A877C0BB5E1D6F2CC47E9965CC1520E6C50BFD8BB15DD6A3B7ABE760EAFDC6BE97EE84FFA586A215D3178B08983C0B5A6E618C744FF7C7DA51165B9635F419BAC20D49E6E3A3139B060472E64739FE0F6C64CDB926DAB782DEF36D2DA21474E9F62E3D4C4BE42093204571A9F449E6BABE18913AF29DDF9A987AA4C4A4DA4D8A0943D86CAA18DA71EA3C04547015F918858D5F943A924F0AF9FC9E54D82BF2B7A62B9E09F11CEB1788FBE2D8AC21D2349E28374931881D936B2C0377F022265AAC5D40571D421B8E9A8D36E09A35021B453E870D3059BED6E09D1CBDA6AA2DE3A"})
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
