#Ruta: src/api/aircrafts_api.py

import requests
import json
from ..schemas.aircrafts_schemas import (
    aircraft_create_schema,
    aircraft_out_schema,
    aircraft_update_schema,
    aircraft_error_schema,
)
from jsonschema import validate, ValidationError
import logging


class AircraftsAPI:
    def __init__(self, token=None):
        """Inicializa la API de aeronaves.
        Si no se pasa token, se toma desde config (archivo .env)."""
        from config.config import config

        self.base_url = config.BASE_URL
        self.aircrafts_endpoint = config.AIRCRAFTS_ENDPOINT
        self.token = token or config.TOKEN
        self.created_aircraft_ids = []

    def _get_headers(self):
        return {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

    def create_aircraft(self, data):
        """Crea una aeronave y devuelve (status_code, dict)"""
        logging.info(f"Creando aeronave con datos: {data}")
        url = f"{self.base_url}{self.aircrafts_endpoint}"
        try:
            response = requests.post(url, headers=self._get_headers(), json=data)
            response_json = response.json() if response.content else {}

            if response.status_code == 201:
                validate(instance=response_json, schema=aircraft_out_schema)
                aircraft_id = response_json.get("id")
                if aircraft_id:
                    self.created_aircraft_ids.append(aircraft_id)
                return response.status_code, response_json
            elif response.status_code == 422:
                validate(instance=response_json, schema=aircraft_error_schema)
                return response.status_code, response_json
            else:
                return response.status_code, response_json

        except (requests.exceptions.RequestException, ValidationError, json.JSONDecodeError) as e:
            logging.error(f"Error al crear aeronave: {e}")
            return response.status_code if "response" in locals() else None, {}

    def get_aircraft_by_id(self, aircraft_id):
        """Obtiene aeronave por ID"""
        url = f"{self.base_url}{self.aircrafts_endpoint}/{aircraft_id}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response_json = response.json() if response.content else {}
            if response.status_code == 200:
                validate(instance=response_json, schema=aircraft_out_schema)
            elif response.status_code == 422:
                validate(instance=response_json, schema=aircraft_error_schema)
            return response.status_code, response_json
        except (requests.exceptions.RequestException, ValidationError, json.JSONDecodeError) as e:
            logging.error(f"Error al obtener aeronave por ID: {e}")
            return response.status_code if "response" in locals() else None, {}

    def get_all_aircrafts(self, params=None):
        """Obtiene todas las aeronaves. Params opcionales: skip, limit"""
        url = f"{self.base_url}{self.aircrafts_endpoint}"
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response_json = response.json() if response.content else []
            if response.status_code == 200:
                if isinstance(response_json, list):
                    for aircraft in response_json:
                        validate(instance=aircraft, schema=aircraft_out_schema)
            elif response.status_code in [422, 500]:
                validate(instance=response_json, schema=aircraft_error_schema)
            return response.status_code, response_json
        except (requests.exceptions.RequestException, ValidationError, json.JSONDecodeError) as e:
            logging.error(f"Error al obtener todas las aeronaves: {e}")
            return response.status_code if "response" in locals() else None, []

    def update_aircraft(self, aircraft_id, data):
        """Modifica una aeronave por ID (PUT)"""
        logging.info(f"Actualizando aeronave {aircraft_id} con datos: {data}")
        url = f"{self.base_url}{self.aircrafts_endpoint}/{aircraft_id}"
        try:
            response = requests.put(url, headers=self._get_headers(), json=data)
            response_json = response.json() if response.content else {}

            # Validación según contrato
            if response.status_code == 200:
                # Permitir propiedad 'id' en respuesta de PUT
                schema = aircraft_update_schema.copy()
                schema["properties"]["id"] = {"type": "string"}
                validate(instance=response_json, schema=schema)
            elif response.status_code == 422:
                validate(instance=response_json, schema=aircraft_error_schema)

            return response.status_code, response_json

        except (requests.exceptions.RequestException, ValidationError, json.JSONDecodeError) as e:
            logging.error(f"Error al actualizar aeronave: {e}")
            return response.status_code if "response" in locals() else None, {}

    def delete_aircraft(self, aircraft_id):
        """Elimina aeronave por ID"""
        url = f"{self.base_url}{self.aircrafts_endpoint}/{aircraft_id}"
        try:
            response = requests.delete(url, headers=self._get_headers())
            if response.status_code in [204, 422]:
                return response.status_code
            else:
                # Validación de error inesperado
                if response.content:
                    try:
                        validate(instance=response.json(), schema=aircraft_error_schema)
                    except ValidationError:
                        logging.error(f"Bug detectado: DELETE aeronave devolvió {response.status_code}")
                return response.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al eliminar aeronave: {e}")
            return None
