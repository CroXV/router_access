from .pages import login, wlan
from .utils.driver import Driver


class DriverManager:

    def __init__(self):
        self.driver = Driver()

        self.login_page = login.LoginPage(self.driver)
        self.settings_page = wlan.WlanSettingsPage(self.driver)
