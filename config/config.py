# Ruta: config/config.py

import os
from dotenv import load_dotenv

# Se carga el archivo .env
load_dotenv()

class Config:
    # URL base del proyecto
    BASE_URL = "https://cf-automation-airline-api.onrender.com"

    # Endpoints principales de autenticación
    SIGNUP_ENDPOINT = "/auth/signup"
    LOGIN_ENDPOINT = "/auth/login"

    # Endpoints de aeronaves
    AIRCRAFTS_ENDPOINT = "/aircrafts"

    # Credenciales admin obtenidas desde el entorno
    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    # Cómo envía el payload de login:
    # True  -> application/x-www-form-urlencoded con campos: username, password
    # False -> application/json con campos: email, password
    LOGIN_AS_FORM = True

# Para mantener compatibilidad con el import actual
config = Config()