# Archivo: tests/test_aircrafts.py

import pytest
import os
from src.helpers.utils import generate_tail_number, validate_json_schema, log_finding
from src.schemas.aircrafts_schemas import aircraft_response_schema
from src.helpers.csv_loader import load_aircrafts_from_csv

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/aircrafts.csv")
rows = load_aircrafts_from_csv(CSV_PATH)

def _extract_id_from_response(resp_json):
    return resp_json.get("id") or resp_json.get("_id") or (resp_json.get("data") or {}).get("id")

# -------------------------
# Fixture parametrizado con CSV
# -------------------------
@pytest.fixture(params=rows)
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
        raise Exception(f"Error creando aeronave para fixture, fila CSV: {row}, status: {response.status_code}")
    yield aircraft_id
    # Cleanup
    del_resp = aircrafts_api.delete_aircraft(aircraft_id)
    if del_resp.status_code not in (200, 204):
        print(f"Cleanup fallido para aeronave {aircraft_id}, status: {del_resp.status_code}")

# -------------------------
# GET
# -------------------------
def test_get_aircraft_by_id(aircrafts_api, create_aircraft_fixture):
    aircraft_id = create_aircraft_fixture
    resp = aircrafts_api.get_aircraft(aircraft_id)
    assert resp.status_code == 200
    valid, err = validate_json_schema(resp.json(), aircraft_response_schema)
    assert valid, f"Esquema inválido: {err}"

# -------------------------
# PUT
# -------------------------
def test_update_aircraft_success(aircrafts_api, create_aircraft_fixture):
    aircraft_id = create_aircraft_fixture
    payload = {"tail_number": generate_tail_number(), "model": "Updated Model", "capacity": 99}
    resp = aircrafts_api.update_aircraft(aircraft_id, payload)
    assert resp.status_code in (200, 201)
    # Verificación
    get_resp = aircrafts_api.get_aircraft(aircraft_id)
    assert get_resp.json().get("model") == "Updated Model"

# -------------------------
# DELETE
# -------------------------
def test_delete_aircraft_success(aircrafts_api, create_aircraft_fixture):
    aircraft_id = create_aircraft_fixture
    del_resp = aircrafts_api.delete_aircraft(aircraft_id)
    assert del_resp.status_code in (200, 204)
