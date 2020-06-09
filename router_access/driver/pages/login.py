from selenium.webdriver.common.keys import Keys

from ..utils.default_gateway import default_gateway


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

        self.default_gateway = f'http://{default_gateway}/'

    def log_in(self, username, password):
        self.driver.geckodriver.get(self.default_gateway)

        loginElement = self.driver.wait_for_element('#logout_span', delay=1)
        loginElement.click()

        usernameElement = self.driver.wait_for_element('input#username')
        passwordElement = self.driver.wait_for_element('input#password')

        usernameElement.send_keys(username)
        passwordElement.send_keys(password)
        passwordElement.send_keys(Keys.RETURN)
