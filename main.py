from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import pandas as pd
import logging

from bs4 import BeautifulSoup


def get_driver_options() -> None:
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--remote-debugging-port=9222")
    chrome_prefs = {}
    driver_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return driver_options


def search_province(driver, province):
    select = Select(driver.find_element("id", "ContentPlaceHolder1_DD_Provincia"))
    select.select_by_visible_text(province)
    driver.find_element("id", "ContentPlaceHolder1_BT_Cercar").click()


def get_colegiat_cards(driver):
    return driver.find_elements(By.CLASS_NAME, "colegiat")


def get_results_for_page(driver):

    # we need to do this because every time we go back the cards object
    # gets unlinked to the driver object, so we need to select them again
    i = 0
    results = list()
    while True: 
        try:

            # find profile card and click on it 
            card = driver.find_elements(By.CLASS_NAME, "colegiat")[i]
            driver.execute_script("arguments[0].click();", card)

            # wait for profile to be loaded
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'colegiat_fitxa'))
            )

            # parse info w/ BeautifulSoup, Selenium is shitty at this
            soup = BeautifulSoup(driver.page_source, "html.parser")
            info = soup.find("div", {"class": "info-colegiat col-sm-10"}).text.split("\n")[1:]
            title = info[0].split('- ')
            nombre = ' '.join(title[0].split('\xa0'))
            print(f"Getting this fucker's info: {nombre}")
            res = {'nombre': nombre, 'numero_colegiado': title[-1]}
            campos = info[1:]
            for c in campos:
                key_val = c.split(': ')
                if key_val[0] in ["Tel", "Situación", "Dirección"]:
                    res[key_val[0]] = key_val[1]
            results.append(res)

            # go back
            driver.back()
            i += 1
        except IndexError:
            print(f"No more cards for index {i}.")
            break
    return results


def go_to_next_page(driver, page):
    """
    Recursive
    """
    paginator = driver.find_element(By.CLASS_NAME, "paginat")
    try:
        print(f'Going to page {page + 1}')
        paginator.find_elements(By.LINK_TEXT, f"{page + 1}")[0].click()
    except Exception as e:
        print(f"Next page not found, trying next set of pages: \n {e}")
        try:
            paginator.find_elements(By.LINK_TEXT, "...")[0].click()
        except:
            raise(f"Next page not found, exiting: \n {e}")


def main(options: Options = get_driver_options()):
    driver = webdriver.Remote(
        'http://0.0.0.0:4444/wd/hub',
        DesiredCapabilities.FIREFOX,
        options=options
    )
    driver.get("https://www.cafbl.cat/ESP/02_ElColegiado/Buscador-Administradores")
    search_province(driver, "Barcelona")
    results = get_results_for_page(driver)
    page = 1
    while True:
        try:
            go_to_next_page(driver, page)
        except: 
            break
        results.extend(get_results_for_page(driver))
        driver.save_screenshot("test.png")
        page += 1
    pd.DataFrame(results).to_csv('barcelona.csv', index=False)
    driver.quit()


if __name__ == "__main__":

    main()
