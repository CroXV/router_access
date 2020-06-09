from .encryption import decode, encode

import json


def retrieve_login():
    try:
        username, password = None, None
        with open('conf.json') as file:
            data = json.load(file)
            username = data['user']
            password = decode(data['key'])
    except FileNotFoundError:
        pass
    finally:
        return username, password


def save_login(user, key):
    with open('conf.json', 'w') as file:
        data = {'user': user, 'key': encode(key)}
        json.dump(data, file)