# tests/test_login_flow.py
import pytest
from src.api.login_api import LoginAPI

TOKEN_BEARER = None  # variable global para compartir entre tests


@pytest.mark.login
def test_login_success():
    global TOKEN_BEARER
    login_api = LoginAPI()
    token, status = login_api.login_user("tester", "1234")
    assert status == 200, "Login fallido"
    assert token is not None, "No se recibió token"

    TOKEN_BEARER = token  # guardamos token globalmente
