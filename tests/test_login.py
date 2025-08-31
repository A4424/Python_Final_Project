#Ruta test/test_login.py
import pytest
import pandas as pd
from src.api.login_api import LoginAPI
from tests.conftest import login_api


@pytest.fixture(scope="module")
def users_data():
    """
    Se lee el archivo CSV y se devuelven los datos como un DataFrame de Pandas.
    """
    return pd.read_csv('data/usuarios/usuarios.csv')


@pytest.mark.happy_path
def test_login_happy_path(login_api, users_data):
    """
    Se prueba el escenario de login exitoso con credenciales correctas.
    """
    happy_path_user = users_data[users_data['is_happy_path'] == True].iloc[0]
    username = happy_path_user['username']
    password = happy_path_user['passwords']

    token, status = login_api.login_user(username, password)

    assert status == 200
    assert isinstance(token, str)
    assert len(token) > 0

@pytest.mark.error
@pytest.mark.parametrize("test_case, expected_status", [
    ("Error - Datos faltantes de usuario 422", 401),
    ("Error - Datos faltantes de clave 422", 401),
    ("Error - Datos faltantes 422", 401),
    # Se corrige la descripción para que coincida con el CSV
    #("Error - De validación 401: Clave incorrecta", 422)
    ("Validar contrato: se espera 422", 422)  # <--- Aquí se realiza el cambio
])

def test_login_error_cases(login_api, users_data, test_case, expected_status):
    """
    Se prueban los escenarios de login con datos de entrada inválidos y de validación.
    """
    error_data = users_data[users_data['description'] == test_case].iloc[0]
    username = error_data['username']
    password = error_data['passwords']

    token, status = login_api.login_user(username, password)

    assert status == expected_status
    assert token is None