import pytest
import pandas as pd
from src.api.aircrafts_api import AircraftsAPI
from config.config import config

# Cargar los datos de prueba desde el archivo CSV
aircrafts_data = pd.read_csv("data/aircrafts/test_data_aircrafts.csv").to_dict(orient="records")

# Instanciar el cliente de la API de aeronaves
aircrafts_api = AircraftsAPI(base_url=config.BASE_URL)


@pytest.mark.parametrize("data", [d for d in aircrafts_data if d['is_happy_path']])
@pytest.mark.happy_path
def test_create_aircraft_happy_path(auth_token, data):
    """
    Prueba el happy path de la creación de una aeronave con datos válidos.
    """
    payload = {
        "tail_number": data["tail_number"],
        "model": data["model"],
        "capacity": int(data["capacity"])
    }

    response = aircrafts_api.create_aircraft(auth_token, payload)

    assert response["status_code"] == 201, f"Código de estado inesperado: {response}"
    assert "tail_number" in response, "La respuesta no contiene 'tail_number'"
    assert response["tail_number"] == data["tail_number"]
    assert response["model"] == data["model"]
    assert response["capacity"] == data["capacity"]


@pytest.mark.parametrize("data", [d for d in aircrafts_data if not d['is_happy_path']])
@pytest.mark.error
def test_create_aircraft_error_cases(auth_token, data):
    """
    Prueba los escenarios de error en la creación de una aeronave.
    """
    payload = {
        "tail_number": data["tail_number"] if pd.notna(data["tail_number"]) else None,
        "model": data["model"] if pd.notna(data["model"]) else None,
        "capacity": int(data["capacity"]) if pd.notna(data["capacity"]) else None
    }

    response = aircrafts_api.create_aircraft(auth_token, payload)

    assert response["status_code"] == 400, f"Se esperaba un error 400, pero se obtuvo: {response['status_code']}"
    assert "error" in response, "La respuesta de error no contiene el campo 'error'"


@pytest.mark.happy_path
def test_get_aircrafts(auth_token):
    """
    Prueba el happy path de obtener todas las aeronaves.
    """
    response = aircrafts_api.get_all_aircrafts(auth_token)

    assert response["status_code"] == 200, f"Se esperaba un código 200, pero se obtuvo: {response['status_code']}"
    assert isinstance(response["data"], list), "La respuesta no es una lista"
    assert len(response["data"]) > 0, "La lista de aeronaves está vacía"


@pytest.mark.happy_path
def test_get_aircraft_by_id(auth_token):
    """
    Prueba el happy path de obtener una aeronave por su ID.
    """
    payload = {
        "tail_number": "N-123-GET",
        "model": "TestModel-GET",
        "capacity": 100
    }
    create_response = aircrafts_api.create_aircraft(auth_token, payload)
    aircraft_id = create_response["id"]

    response = aircrafts_api.get_aircraft_by_id(auth_token, aircraft_id)

    assert response["status_code"] == 200, f"Se esperaba un código 200, pero se obtuvo: {response['status_code']}"
    assert response["tail_number"] == payload["tail_number"]
    assert response["model"] == payload["model"]
    assert response["id"] == aircraft_id

    aircrafts_api.delete_aircraft(auth_token, aircraft_id)


@pytest.mark.happy_path
def test_update_aircraft(auth_token):
    """
    Prueba el happy path de la actualización de una aeronave.
    """
    # Se crea una aeronave para actualizar
    initial_payload = {
        "tail_number": "N-UPDATE-01",
        "model": "InitialModel",
        "capacity": 150
    }
    create_response = aircrafts_api.create_aircraft(auth_token, initial_payload)
    aircraft_id = create_response["id"]

    # Se preparan los nuevos datos
    update_payload = {
        "tail_number": "N-UPDATED-01",
        "model": "UpdatedModel",
        "capacity": 200
    }

    # Se hace la solicitud PUT
    response = aircrafts_api.update_aircraft(auth_token, aircraft_id, update_payload)

    # Se valida la respuesta
    assert response["status_code"] == 200, f"Se esperaba un código 200, pero se obtuvo: {response['status_code']}"
    assert response["tail_number"] == update_payload["tail_number"]
    assert response["model"] == update_payload["model"]
    assert response["capacity"] == update_payload["capacity"]
    assert response["id"] == aircraft_id

    # Se elimina la aeronave de prueba
    aircrafts_api.delete_aircraft(auth_token, aircraft_id)


@pytest.mark.happy_path
def test_delete_aircraft(auth_token):
    """
    Prueba el happy path de la eliminación de una aeronave.
    """
    # Se crea una aeronave para eliminar
    payload = {
        "tail_number": "N-DELETE-01",
        "model": "TestModel-DELETE",
        "capacity": 120
    }
    create_response = aircrafts_api.create_aircraft(auth_token, payload)
    aircraft_id = create_response["id"]

    # Se hace la solicitud DELETE
    response = aircrafts_api.delete_aircraft(auth_token, aircraft_id)

    # Se valida la respuesta
    assert response["status_code"] == 200, f"Se esperaba un código 200, pero se obtuvo: {response['status_code']}"
    assert "message" in response
    assert response["message"] == "Aircraft deleted successfully"

    # Se valida que la aeronave no se pueda obtener
    get_response = aircrafts_api.get_aircraft_by_id(auth_token, aircraft_id)
    assert get_response["status_code"] == 404, "La aeronave no fue eliminada correctamente"