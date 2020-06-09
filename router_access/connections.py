from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from router_access.misc import wait_for_element

import time
import sys
import os


class Browser:

    def __init__(self):
        self.driver = None

        # Home NavBar
        self.settingsPage = 'http://192.168.8.1/html/ethernetsettings.html'

        # WlanSettings
        self.basicSettings = 'http://192.168.8.1/html/wlanbasicsettings.html'

    def start_driver(self):
        homePage = 'http://192.168.8.1/'
        options = Options()
        options.headless = True

        self.driver = webdriver.Firefox(self.resource_path('./driver/'), options=options)
        self.driver.implicitly_wait(5)
        self.driver.get(homePage)

    @staticmethod
    def resource_path(relative_path):
        base_path = None
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        finally:
            return os.path.join(base_path, relative_path)

    def quit_driver(self):
        while self.driver is None:
            time.sleep(5)
        self.driver.quit()

    def login(self, username, password):
        loginElement = wait_for_element(self.driver, '#logout_span', delay=1)
        loginElement.click()

        usernameElement = wait_for_element(self.driver, 'input#username')
        passwordElement = wait_for_element(self.driver, 'input#password')

        usernameElement.send_keys(username)
        passwordElement.send_keys(password)
        passwordElement.send_keys(Keys.RETURN)

        time.sleep(2)
        self.driver.get(self.settingsPage)

    def toggleWifi(self):
        self.driver.get(self.basicSettings)
        time.sleep(1)

        toggleOnElement = wait_for_element(self.driver, '#wlan_turn_on')
        toggleOffElement = wait_for_element(self.driver, '#wlan_turn_off')

        applySettingsElement = wait_for_element(self.driver, '#apply_button')

        if toggleOnElement.is_selected():
            toggleOffElement.click()
        else:
            toggleOnElement.click()

        applySettingsElement.click()