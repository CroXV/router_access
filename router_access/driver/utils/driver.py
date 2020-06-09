import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .resource_path import resource_path


class Driver:

    geckodriver = None

    options = Options()
    options.headless = True

    @staticmethod
    def start_driver():
        Driver.geckodriver = webdriver.Firefox(
            resource_path('./geckodriver/'),
            options=Driver.options,
            log_path=os.devnull
        )
        Driver.geckodriver.implicitly_wait(5)

    @staticmethod
    def exit_driver():
        while not Driver.geckodriver:
            time.sleep(2)
        Driver.geckodriver.quit()

    @staticmethod
    def wait_for_element(css_selector, wait=20, delay=0):
        try:
            WebDriverWait(Driver.geckodriver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            time.sleep(delay)
        except TimeoutError:
            Driver.geckodriver.quit()

        return Driver.geckodriver.find_element_by_css_selector(css_selector)
