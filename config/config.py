# Ruta: config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://cf-automation-airline-api.onrender.com"
    SIGNUP_ENDPOINT = "/auth/signup"
    LOGIN_ENDPOINT = "/auth/login"
    AIRCRAFTS_ENDPOINT = "/aircrafts"

    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    LOGIN_AS_FORM = True  # True -> x-www-form-urlencoded, False -> JSON

config = Config()
