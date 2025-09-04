# # Ruta: test/conftest.py - Detecta fallo en el contrato.
# import pytest
# import pandas as pd
# from src.api.login_api import LoginAPI
#
# @pytest.fixture(scope="session")
# def login_api():
#     return LoginAPI()
#
# @pytest.fixture(scope="session")
# def login_token(login_api):
#     # Usuario válido de prueba
#     username = "admin@demo.com"
#     password = "admin123"
#     token, status = login_api.login_user(username, password)
#     if not token:
#         pytest.skip("No se pudo obtener token válido para los tests")
#     return token
#
# @pytest.fixture(scope="session")
# def users_data():
#     # Leer CSV con casos de login
#     return pd.read_csv("tests/data/users_login.csv")

######## Ruta: test/conftest.py - Detectado el fallo en el contrato. Asume el fallo y deja pasar. ##################
# import pytest
# import pandas as pd
# from src.api.login_api import LoginAPI
# from src.api.aircrafts_api import AircraftsAPI
#
# # Fixture para login API
# @pytest.fixture(scope="session")
# def login_api():
#     return LoginAPI()
#
# # Fixture para token
# @pytest.fixture(scope="session")
# def login_token(login_api):
#     username = "admin@demo.com"
#     password = "admin123"
#     token, status = login_api.login_user(username, password)
#     if not token:
#         pytest.skip("No se pudo obtener token válido")
#     return token
#
# # Fixture para usuarios de login (CSV)
# @pytest.fixture(scope="session")
# def users_data():
#     return pd.read_csv("tests/data/users_login.csv")
#
# # Fixture para Aircrafts API
# @pytest.fixture(scope="session")
# def aircrafts_api():
#     return AircraftsAPI()
#
# # Fixture para datos de aeronaves de prueba
# @pytest.fixture(scope="session")
# def aircraft_data():
#     return {
#         "tail_number": "ABC123",
#         "model": "Boeing 737",
#         "capacity": 180
#     }
#
# # Registrar marca order para evitar warnings
# def pytest_configure(config):
#     config.addinivalue_line(
#         "markers", "order(order_number): mark test to run in order"
#     )
#
#############
import pytest
import pandas as pd
from src.api.login_api import LoginAPI
from src.api.aircrafts_api import AircraftsAPI

# Fixture para login API
@pytest.fixture(scope="session")
def login_api():
    return LoginAPI()

# Fixture para token
@pytest.fixture(scope="session")
def login_token(login_api):
    username = "admin@demo.com"
    password = "admin123"
    token, status = login_api.login_user(username, password)
    if not token:
        pytest.skip("No se pudo obtener token válido")
    return token

# Fixture para usuarios de login (CSV)
@pytest.fixture(scope="session")
def users_data():
    return pd.read_csv("tests/data/users_login.csv")

# Fixture para Aircrafts API (con token)
@pytest.fixture(scope="session")
def aircrafts_api(login_token):
    return AircraftsAPI(token=login_token)

# Fixture para datos de aeronaves de prueba
@pytest.fixture(scope="session")
def aircraft_data():
    return {
        "tail_number": "ABC123",
        "model": "Boeing 737",
        "capacity": 180
    }

# Registrar marca order para evitar warnings
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "order(order_number): mark test to run in order"
    )

