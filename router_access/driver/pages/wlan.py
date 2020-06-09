import time


class WlanSettingsPage:

    def __init__(self, driver):
        self.driver = driver

        self.basic_settings_url = 'http://192.168.8.1/html/wlanbasicsettings.html'

    def toggle_wifi(self, update_status):
        self.driver.geckodriver.get(self.basic_settings_url)

        toggleOnElement = self.driver.wait_for_element('#wlan_turn_on')
        toggleOffElement = self.driver.wait_for_element('#wlan_turn_off')

        applySettingsElement = self.driver.wait_for_element('#apply_button')

        if not toggleOnElement.is_selected():
            update_status.emit('On')
            toggleOnElement.click()
        else:
            update_status.emit('Off')
            toggleOffElement.click()

        applySettingsElement.click()

        time.sleep(1.2)
