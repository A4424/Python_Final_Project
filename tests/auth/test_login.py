
"""
Incluye: éxito + validaciones negativas + verificación del token con /users/me.
Para el caso exitoso, creo un usuario único con SignupAPI (como hiciste en signup) y luego pruebo el login con ese usuario.
En errores, cubro credenciales incorrectas, usuario inexistente y payload inválido.
"""
import uuid
import pytest

# from config import config as project_config No funicona
# tests/auth/test_login.py
from config.config import config as project_config


from src.api.signup_api import SignupAPI
from src.api.login_api import LoginAPI
from src.api.users_api import UsersAPI


# ---------- Fixtures ----------

@pytest.fixture(scope="session")
def base_url():
    return project_config.BASE_URL


@pytest.fixture(scope="session")
def signup_client(base_url):
    return SignupAPI(base_url)


@pytest.fixture(scope="session")
def login_client(base_url):
    return LoginAPI(
        base_url=base_url,
        endpoint=project_config.LOGIN_ENDPOINT,
        as_form=project_config.LOGIN_AS_FORM
    )


@pytest.fixture(scope="session")
def users_client(base_url):
    return UsersAPI(
        base_url=base_url,
        me_endpoint=project_config.USERS_ME_ENDPOINT
    )


@pytest.fixture
def fresh_user(signup_client):
    """
    Crea un usuario nuevo vía signup para usar en pruebas de login.
    Retorna (email, password, full_name).
    """
    unique_email = f"qa_login_{uuid.uuid4()}@example.com"
    password = "Secure_password_123"
    user = {
        "email": unique_email,
        "password": password,
        "full_name": "QA Login User"
    }
    resp = signup_client.signup_user(user)

    # En algunas APIs, si el usuario existiera, podría devolver 400/409.
    # Este assert es conservador: exige un id en la respuesta de éxito.
    assert "id" in resp, f"Fallo al crear usuario para login: {resp}"
    return unique_email, password, user["full_name"]


# ---------- Tests ----------

@pytest.mark.smoke
def test_login_success_and_validate_me(fresh_user, login_client, users_client):
    """
    1) Login exitoso
    2) Validar formato del token
    3) Llamar a /users/me con el token y comprobar identidad
    """
    email, password, _ = fresh_user

    login_resp = login_client.login_user(identifier=email, password=password)

    # Validaciones básicas de login
    assert "error" not in login_resp, f"Login devolvió error: {login_resp}"
    assert login_resp.get("status_code") == 200, f"Status inesperado: {login_resp}"
    # Nombres de campos habituales: access_token / token_type
    assert "access_token" in login_resp, f"Falta access_token: {login_resp}"
    assert login_resp.get("access_token"), "El access_token está vacío"
    if "token_type" in login_resp:
        assert login_resp["token_type"].lower() == "bearer"

    # Validar token con /users/me
    token = login_resp["access_token"]
    me_resp = users_client.get_me(token)

    assert "error" not in me_resp, f"/users/me devolvió error: {me_resp}"
    assert me_resp.get("status_code") == 200
    assert me_resp.get("email") == email, f"El email de /users/me no coincide: {me_resp}"


def test_login_with_wrong_password(fresh_user, login_client):
    email, _password, _ = fresh_user
    wrong_pass = "totally_wrong_password"

    resp = login_client.login_user(identifier=email, password=wrong_pass)

    # Códigos esperados típicos: 401 Unauthorized (o 400 según backend)
    assert resp.get("status_code") in (400, 401), f"Status inesperado: {resp}"
    assert "error" in resp, "Debería existir mensaje de error para credenciales inválidas"


def test_login_non_existing_user(login_client):
    email = f"not_exists_{uuid.uuid4()}@example.com"
    password = "AnyPass123"

    resp = login_client.login_user(identifier=email, password=password)

    # Códigos esperados típicos: 401 o 404
    assert resp.get("status_code") in (401, 404), f"Status inesperado: {resp}"
    assert "error" in resp, "Debería existir mensaje de error para usuario inexistente"


def test_login_invalid_payload(login_client):
    """
    Si el contrato es form-data: enviar username vacío o password vacío debe dar 422.
    Si el contrato es JSON: email inválido o string vacío.
    """
    if login_client.as_form:
        # Campos requeridos vacíos
        resp = login_client.login_user(identifier="", password="")
    else:
        # Email inválido en JSON
        resp = login_client.login_user(identifier="invalid-email", password="x")

    # Validación típica de FastAPI/Pydantic
    assert resp.get("status_code") in (400, 422), f"Status inesperado: {resp}"
    assert "error" in resp, "Debería existir mensaje de error por validación"
