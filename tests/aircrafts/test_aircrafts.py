# File: tests/aircrafts/test_aircrafts.py
import pytest
import random
import csv
from src.api.aircrafts_api import AircraftsAPI

# -------------------------------
# Función para cargar datos desde CSV
# -------------------------------
def load_aircraft_data_from_csv(file_path):
    data_list = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos capacity a int si es posible
            try:
                row["capacity"] = int(row["capacity"])
            except ValueError:
                pass
            row["expected_status"] = int(row["expected_status"])
            data_list.append(row)
    return data_list

# -------------------------------
# Fixture que proporciona datos del CSV
# -------------------------------
@pytest.fixture(scope="session")
def aircraft_data_list():
    return load_aircraft_data_from_csv("tests/data/aircrafts.csv")

# -------------------------------
# Fixture que crea la instancia de AircraftsAPI
# -------------------------------
@pytest.fixture(scope="session")
def aircrafts_api(login_token):
    return AircraftsAPI(token=login_token)

# -------------------------------
# Test de creación de aeronaves
# -------------------------------
@pytest.mark.create
@pytest.mark.parametrize("aircraft_data", load_aircraft_data_from_csv("tests/data/aircrafts.csv"))
def test_create_aircrafts(aircrafts_api, aircraft_data):
    # Hacemos tail_number único
    if aircraft_data.get("tail_number"):
        aircraft_data["tail_number"] = f"{aircraft_data['tail_number']}{random.randint(1000,9999)}"

    status, created = aircrafts_api.create_aircraft(aircraft_data)
    print(f"DEBUG CREATE: status={status}, response={created}")

    assert status == aircraft_data["expected_status"], f"Esperado {aircraft_data['expected_status']}, recibido {status}"

    if status == 201:
        assert created.get("model") == aircraft_data["model"]
        assert created.get("capacity") == aircraft_data["capacity"]
        assert created.get("tail_number") == aircraft_data["tail_number"]
        assert "id" in created

        # Cleanup
        aircrafts_api.delete_aircraft(created["id"])

# -------------------------------
# Test de consulta por ID
# -------------------------------
@pytest.mark.read
def test_get_aircraft_by_id(aircrafts_api):
    data = {"model": "TestModel", "capacity": 150, "tail_number": f"TST{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    assert status == 201, f"No se pudo crear aeronave: status={status}"
    aircraft_id = created["id"]

    status, result = aircrafts_api.get_aircraft_by_id(aircraft_id)
    print(f"DEBUG GET: status={status}, response={result}")
    assert status == 200
    assert result["id"] == aircraft_id
    assert result["model"] == data["model"]

    # Cleanup
    aircrafts_api.delete_aircraft(aircraft_id)

# -------------------------------
# Test de listado
# -------------------------------
@pytest.mark.read
def test_get_all_aircrafts(aircrafts_api):
    status, result = aircrafts_api.get_all_aircrafts()
    print(f"DEBUG LIST: status={status}, response={result}")
    assert status == 200
    assert isinstance(result, list)

# -------------------------------
# Test de actualización
# -------------------------------
@pytest.mark.update
def test_update_aircraft(aircrafts_api):
    data = {"model": "ModTest", "capacity": 120, "tail_number": f"MOD{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    assert status == 201, f"No se pudo crear aeronave: status={status}"
    aircraft_id = created["id"]

    new_data = {"model": "ModTestUpdated", "capacity": 200, "tail_number": data["tail_number"]}
    status, updated = aircrafts_api.update_aircraft(aircraft_id, new_data)
    print(f"DEBUG UPDATE: status={status}, response={updated}")
    assert status == 200
    assert updated["capacity"] == 200
    assert updated["model"] == "ModTestUpdated"

    # Cleanup
    aircrafts_api.delete_aircraft(aircraft_id)

# -------------------------------
# Test de eliminación
# -------------------------------
@pytest.mark.delete
def test_delete_aircraft(aircrafts_api):
    data = {"model": "DelTest", "capacity": 110, "tail_number": f"DEL{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    assert status == 201, f"No se pudo crear aeronave: status={status}"
    aircraft_id = created["id"]

    status = aircrafts_api.delete_aircraft(aircraft_id)
    print(f"DEBUG DELETE: status={status}")
    assert status == 204
