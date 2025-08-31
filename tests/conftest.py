import pytest
from src.api.login_api import LoginAPI
from config.config import config

@pytest.fixture(scope="session")
def login_api():
    """
    Se crea una instancia de LoginAPI para la sesión de pruebas.
    """
    return LoginAPI()

@pytest.fixture(scope="session")
def login_token(login_api):
    """
    Se obtiene un token de acceso de la API de login.
    Este token se comparte con todos los tests de la sesión.
    """
    print("\nObteniendo token de login...")
    token, status_code = login_api.login_user(config.ADMIN_USER, config.ADMIN_PASSWORD)
    if status_code != 200:
        pytest.fail(f"Fallo en la obtención del token de login con estado: {status_code}")
    print("Token obtenido con éxito.")
    return token