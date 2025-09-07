#CODIGO NUEVO tests/test_login_contract.py
import pytest
import requests
from src.api.login_api import LoginAPI
from config.config import config

# -----------------------------
# Fixture para login exitoso
# -----------------------------
@pytest.fixture(scope="session")
def auth_header():
    login_api = LoginAPI()
    login_api.login()
    return login_api.get_auth_header()

# -----------------------------
# Test de login correcto
# -----------------------------
def test_login_success(auth_header):
    if not auth_header or "Authorization" not in auth_header:
        from src.helpers.utils import log_finding
        log_finding(
            title="Login exitoso - Contrato",
            endpoint=f"{config.BASE_URL}{config.LOGIN_ENDPOINT}",
            expected="Token Bearer",
            actual="No token",
            response_body={},
            motivo="Motivo: login correcto no devuelve token"
        )

# -----------------------------
# Test de errores de validación (datos faltantes)
# -----------------------------
@pytest.mark.parametrize("payload, description", [
    ({}, "Login sin username ni password"),
    ({"username": config.ADMIN_USER}, "Login sin password"),
    ({"password": config.ADMIN_PASSWORD}, "Login sin username"),
])
def test_login_validation_422(payload, description):
    url = f"{config.BASE_URL}{config.LOGIN_ENDPOINT}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 422:
        from src.helpers.utils import log_finding
        try:
            body = response.json()
        except Exception:
            body = {"text": response.text}
        log_finding(
            title=f"POST /login - {description}",
            endpoint=url,
            expected="422 Unprocessable Entity",
            actual=str(response.status_code),
            response_body=body,
            motivo=f"Motivo: error de validación en login - {description}"
        )

# -----------------------------
# Test de credenciales incorrectas
# -----------------------------
def test_login_incorrect_credentials():
    payload = {"username": "wrong@demo.com", "password": "wrongpass"}
    url = f"{config.BASE_URL}{config.LOGIN_ENDPOINT}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 422:
        from src.helpers.utils import log_finding
        try:
            body = response.json()
        except Exception:
            body = {"text": response.text}
        log_finding(
            title="POST /login - Credenciales incorrectas",
            endpoint=url,
            expected="422 Unprocessable Entity",
            actual=str(response.status_code),
            response_body=body,
            motivo="Motivo: credenciales incorrectas (undocumented si no devuelve 422)"
        )
