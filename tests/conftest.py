import pytest
from src.api.login_api import LoginAPI
from config.config import config

@pytest.fixture(scope="session")
def auth_token():
    """
    Fixture para obtener un token de autenticación de admin, una sola vez por sesión.
    """
    login_api = LoginAPI(base_url=config.BASE_URL, as_form=config.LOGIN_AS_FORM)
    response = login_api.login_user(config.ADMIN_USER, config.ADMIN_PASSWORD)

    if "access_token" not in response:
        pytest.fail(f"Fallo al obtener el token de autenticación: {response}")

    return response["access_token"]