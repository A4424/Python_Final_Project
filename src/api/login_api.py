# Ruta src/api/login_api.py
import requests
from config.config import config

class LoginAPI:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.login_endpoint = config.LOGIN_ENDPOINT

    def login(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{self.base_url}{self.login_endpoint}", json=payload)
        return response


