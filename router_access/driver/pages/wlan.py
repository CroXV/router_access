import time


class WlanSettingsPage:

    def __init__(self, driver):
        self.driver = driver

        self.basic_settings_url = 'http://192.168.8.1/html/wlanbasicsettings.html'

    def toggle_wifi(self, status):
        if not self.basic_settings_url == self.driver.geckodriver.current_url:
            status.emit('Initializing engine')
            self.driver.geckodriver.get(self.basic_settings_url)

        time.sleep(0.4)

        self.toggle_on_element = self.driver.wait_for_element('#wlan_turn_on')
        self.toggle_off_element = self.driver.wait_for_element('#wlan_turn_off')

        self.applySettingsElement = self.driver.wait_for_element('#apply_button')

        if not self.toggle_on_element.is_selected():
            status.emit('Turning Wifi On..')
            self.toggle_on_element.click()
        else:
            status.emit('Turning Wifi Off..')
            self.toggle_off_element.click()

        self.applySettingsElement.click()

        dialog_close_element = self.driver.wait_for_element('#showInfoCanvas')
        dialog_close_element.click()

        time.sleep(1.2)

        status.emit('Done')
