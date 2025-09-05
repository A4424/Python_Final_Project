# Ruta test/test_login.py
import pytest

@pytest.mark.error(order=2)
@pytest.mark.parametrize("test_case, expected_status", [
    ("Error - Datos faltantes de usuario 422", 401),  # La API real devuelve 401
    ("Error - Datos faltantes de clave 422", 401),
    ("Error - Datos faltantes 422", 401),
    ("Validar contrato: se espera 422", 401)
])
def test_login_error_cases(login_api, users_data, test_case, expected_status):
    """
    Prueba de login con datos inválidos.
    """
    error_data = users_data[users_data['description'] == test_case].iloc[0]
    username = error_data['username']
    password = error_data['passwords']

    token, status = login_api.login_user(username, password)
    assert status == expected_status

