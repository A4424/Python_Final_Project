import pytest
from src.api.login_api import LoginAPI
from src.api.aircrafts_api import AircraftsAPI
from src.helpers.utils import generate_tail_number
import csv
import os
from dotenv import load_dotenv

# -------------------------
# Cargar variables de entorno desde .env
# -------------------------
load_dotenv()  # Esto carga ADMIN_USER y ADMIN_PASSWORD

# -------------------------
# Función para extraer ID de la respuesta JSON
# -------------------------
def _extract_id_from_response(response_json):
    """
    Extrae el campo 'id' de la respuesta JSON de la API.
    """
    return response_json.get("id")

# -------------------------
# Fixture para API de login
# -------------------------
@pytest.fixture(scope="session")
def login_api():
    return LoginAPI()

# -------------------------
# Fixture para token válido usando variables de entorno
# -------------------------
@pytest.fixture(scope="session")
def login_token(login_api):
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        raise Exception("No se encontraron credenciales en el .env")

    response = login_api.login(username, password)
    if response.status_code != 200:
        raise Exception(f"Login fallido: {response.status_code} - {response.text}")
    return response.json().get("access_token")

# -------------------------
# Fixture para API de aeronaves
# -------------------------
@pytest.fixture(scope="session")
def aircrafts_api(login_token):
    api = AircraftsAPI()
    api.set_token(login_token)  # Necesitamos que AircraftsAPI tenga este método
    return api

# -------------------------
# Cargar datos desde CSV
# -------------------------
def load_aircraft_rows(csv_path="tests/data/aircrafts.csv"):
    rows = []
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV: {csv_path}")

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

# -------------------------
# Fixture para crear aeronaves usando los datos del CSV
# -------------------------
@pytest.fixture(params=load_aircraft_rows())
def create_aircraft_fixture(request, aircrafts_api):
    row = request.param
    payload = {
        "tail_number": row["tail_number"] if row["tail_number"] else generate_tail_number(),
        "model": row["model"],
        "capacity": int(row["capacity"])
    }
    response = aircrafts_api.create_aircraft(payload)
    aircraft_id = _extract_id_from_response(response.json())

    if response.status_code not in (200, 201) or aircraft_id is None:
        raise Exception(
            f"Error creando aeronave para fixture, fila CSV: {row}, status: {response.status_code}, response: {response.text}"
        )

    return {"id": aircraft_id, "data": payload}
