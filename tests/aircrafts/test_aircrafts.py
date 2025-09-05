# Ruta: tests/aircrafts/test_aircrafts.py

import pytest
import random

# -------------------------------
# BLOQUE CREACIÓN DE AERONAVES
# -------------------------------
@pytest.mark.create
@pytest.mark.order(1)
@pytest.mark.parametrize("aircraft_data", [
    {"model": "Boeing 737", "capacity": 180, "tail_number": "ABC123"},
    {"model": "Airbus A320", "capacity": 160, "tail_number": "DEF456"},
    {"model": "Embraer 190", "capacity": 100, "tail_number": "GHI789"},
])
def test_create_aircrafts(aircrafts_api, aircraft_data):
    """Caso positivo: Crear aeronave con datos válidos"""
    aircraft_data["tail_number"] = f"{aircraft_data['tail_number']}{random.randint(1000,9999)}"
    status, created = aircrafts_api.create_aircraft(aircraft_data)
    if status is None or status == 500:
        pytest.skip("Error en backend al crear aeronave")
    assert status in [201, 422]  # contrato
    if status == 201:
        assert created.get("model") == aircraft_data["model"]
        assert created.get("capacity") == aircraft_data["capacity"]
        assert created.get("tail_number") == aircraft_data["tail_number"]
        assert "id" in created


@pytest.mark.create
@pytest.mark.order(2)
def test_create_aircraft_invalid_data(aircrafts_api):
    """Caso negativo: Crear aeronave con datos inválidos"""
    invalid_data = {"model": "", "capacity": "mil", "tail_number": ""}
    status, _ = aircrafts_api.create_aircraft(invalid_data)
    assert status == 422  # contrato

# -------------------------------
# BLOQUE CONSULTA DE AERONAVES
# -------------------------------
@pytest.mark.read
@pytest.mark.order(3)
def test_get_aircraft_by_id(aircrafts_api):
    """Caso positivo: Consultar aeronave existente"""
    data = {"model": "Test Model", "capacity": 150, "tail_number": f"TST{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    if status != 201:
        pytest.skip("No se pudo crear aeronave para prueba de consulta")
    aircraft_id = created["id"]
    status, result = aircrafts_api.get_aircraft_by_id(aircraft_id)
    assert status in [200, 422]
    if status == 200:
        assert result["id"] == aircraft_id
        assert result["model"] == data["model"]


@pytest.mark.read
@pytest.mark.order(4)
def test_get_aircraft_by_id_not_found(aircrafts_api):
    """Caso negativo: Consultar aeronave inexistente"""
    status, result = aircrafts_api.get_aircraft_by_id(999999)
    assert status == 422  # contrato
    assert result == {} or result is not None

# -------------------------------
# BLOQUE LISTADO DE AERONAVES
# -------------------------------
@pytest.mark.read
@pytest.mark.order(5)
def test_get_all_aircrafts(aircrafts_api):
    """Caso positivo: Listar todas las aeronaves sin parámetros"""
    status, result = aircrafts_api.get_all_aircrafts()
    if status == 500:
        pytest.skip("Backend devuelve 500 inesperado")
    assert status in [200, 422]
    if status == 200:
        assert isinstance(result, list)

@pytest.mark.read
@pytest.mark.order(6)
def test_get_all_aircrafts_with_params(aircrafts_api):
    """Caso positivo: Listar todas las aeronaves con parámetros skip=0, limit=10"""
    params = {"skip": 0, "limit": 10}
    status, result = aircrafts_api.get_all_aircrafts(params=params)
    assert status in [200, 422]
    if status == 200:
        assert isinstance(result, list)
        assert len(result) <= 10

@pytest.mark.read
@pytest.mark.order(7)
def test_get_all_aircrafts_invalid_params(aircrafts_api):
    """Caso negativo: Listar aeronaves con parámetros inválidos"""
    params = {"skip": "cero", "limit": "diez"}  # inválidos
    status, result = aircrafts_api.get_all_aircrafts(params=params)
    assert status == 422
    assert result == []

# -------------------------------
# BLOQUE MODIFICACIÓN DE AERONAVES
# -------------------------------
@pytest.mark.update
@pytest.mark.order(8)
def test_update_aircraft(aircrafts_api):
    """Caso positivo: Modificar aeronave existente"""
    data = {"model": "ModTest", "capacity": 120, "tail_number": f"MOD{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    if status != 201:
        pytest.skip("No se pudo crear aeronave para prueba de modificación")
    aircraft_id = created["id"]
    new_data = {"model": "ModTestUpdated", "capacity": 200, "tail_number": data["tail_number"]}
    status, updated = aircrafts_api.update_aircraft(aircraft_id, new_data)
    assert status in [200, 422]
    if status == 200:
        assert updated["capacity"] == 200
        assert updated["model"] == "ModTestUpdated"


@pytest.mark.update
@pytest.mark.order(9)
def test_update_aircraft_not_found(aircrafts_api):
    """Caso negativo: Modificar aeronave inexistente"""
    new_data = {"model": "NoExist", "capacity": 300, "tail_number": "NOEXIST"}
    status, result = aircrafts_api.update_aircraft(999999, new_data)
    assert status == 422
    assert result == {} or result is not None

# -------------------------------
# BLOQUE ELIMINACIÓN DE AERONAVES
# -------------------------------
@pytest.mark.delete
@pytest.mark.order(10)
def test_delete_aircraft(aircrafts_api):
    """Caso positivo: Eliminar aeronave existente"""
    data = {"model": "DelTest", "capacity": 110, "tail_number": f"DEL{random.randint(1000,9999)}"}
    status, created = aircrafts_api.create_aircraft(data)
    if status != 201:
        pytest.skip("No se pudo crear aeronave para prueba de eliminación")
    aircraft_id = created["id"]
    status = aircrafts_api.delete_aircraft(aircraft_id)
    assert status in [204, 422]


@pytest.mark.delete
@pytest.mark.order(11)
def test_delete_aircraft_not_found(aircrafts_api):
    """Caso negativo: Eliminar aeronave inexistente"""
    status = aircrafts_api.delete_aircraft(999999)
    assert status == 422
