from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import logging


def get_chrome_options() -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def main(chrome_options: Options):
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(800, 600)
        driver.get("http://www.ciudadela.eu")
        time.sleep(5)
    except Exception as shit:
        logging.error(f"{shit} happened.")
        return None
    finally:
        driver.quit()


if __name__ == "__main__":

    from selenium.webdriver.common.desired_capabilities import (
        DesiredCapabilities
    )
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        'http://selenium:4444/wd/hub',
        DesiredCapabilities.FIREFOX,
        options=get_chrome_options()
    )
    driver.get("http://www.ciudadela.eu")
    driver.quit()
