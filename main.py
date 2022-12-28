from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


LOGGER = set_logger("selenium_stats")


def get_chrome_options() -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def main(chrome_options: Options) -> None:
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(800, 600)
        driver.get('https://www.ciudadela.eu/')
        time.sleep(5)
        return None
    except Exception as shit:
        LOGGER.error(f"{shit} happened.")
        return None
    finally:
        driver.quit()
