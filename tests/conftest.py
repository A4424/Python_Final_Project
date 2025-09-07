# # Ruta: test/conftest.py
# conftest.py (en la raíz del proyecto)

# tests/conftest.py

import os
import pytest
import pandas as pd
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

from src.api.login_api import LoginAPI
from src.api.aircrafts_api import AircraftsAPI

# -------------------------------
# Fixture: login API
# -------------------------------
@pytest.fixture(scope="session")
def login_api():
    return LoginAPI()

# -------------------------------
# Fixture: token de login
# -------------------------------
@pytest.fixture(scope="session")
def login_token(login_api):
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        pytest.skip("Usuario o contraseña no definidos en .env")

    token, status = login_api.login_user(username, password)
    if not token:
        pytest.skip("No se pudo obtener token válido")
    return token

# -------------------------------
# Fixture: Aircrafts API con token
# -------------------------------
@pytest.fixture(scope="session")
def aircrafts_api(login_token):
    return AircraftsAPI(token=login_token)

# -------------------------------
# Fixture: datos de aeronaves desde CSV
# -------------------------------
@pytest.fixture(scope="session")
def aircrafts_data():
    csv_path = "tests/data/aircrafts.csv"
    if not os.path.exists(csv_path):
        pytest.skip(f"No se encuentra el CSV en {csv_path}")

    df = pd.read_csv(csv_path)

    # Convertir capacity y expected_status a int, si es posible
    for col in ["capacity", "expected_status"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Retorna lista de dicts
    return df.to_dict(orient="records")

# -------------------------------
# Fixture: usuarios desde CSV (login)
# -------------------------------
@pytest.fixture(scope="session")
def users_data():
    csv_path = "tests/data/users_login.csv"
    if not os.path.exists(csv_path):
        pytest.skip(f"No se encuentra el CSV en {csv_path}")
    return pd.read_csv(csv_path)

# -------------------------------
# Configuración de marca 'order'
# -------------------------------
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "order(order_number): mark test to run in order"
    )



