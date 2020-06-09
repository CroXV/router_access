from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

import base64


def wait_for_element(driver, css_selector, wait=20, delay=0):
    try:
        WebDriverWait(driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        time.sleep(delay)
    except TimeoutError:
        driver.quit()

    return driver.find_element_by_css_selector(css_selector)


def retrieve_login():
    try:
        username, password = None, None
        with open('conf.json') as file:
            data = json.load(file)
            username = data['username']
            password = decode_password(data['password'])
    except FileNotFoundError:
        pass
    finally:
        return username, password


def save_login(username, password):
    with open('conf.json', 'w') as file:
        data = {'username': username, 'password': encode_password(password)}
        json.dump(data, file)


def encode_password(password):
    byte = password.encode('utf-8')     # turn password into bytes
    enc = list(base64.b64encode(byte))  # store base 64 encoding in a list

    return enc


def decode_password(password):
    enc_pass = ''.join(chr(b) for b in password).encode('utf-8')
    dec_pass = base64.b64decode(enc_pass)
    str_pass = str(dec_pass, 'utf-8')

    return str_pass