# Ruta: src/api/aircrafts_api.py


import requests
import json
from ..schemas.aircrafts_schemas import aircraft_create_schema, aircraft_out_schema
from jsonschema import validate, ValidationError
import logging

class AircraftsAPI:
    def __init__(self, token=None):
        """Inicializa la API de aeronaves.
        Si no se pasa token, se toma desde config (archivo .env)."""
        from config.config import config
        self.base_url = config.BASE_URL
        self.aircrafts_endpoint = config.AIRCRAFTS_ENDPOINT
        self.token = token or config.TOKEN  # token opcional, por defecto toma de .env
        self.created_aircraft_ids = []

    def create_aircraft(self, data):
        """Crea una aeronave y devuelve (status_code, dict)"""
        logging.info(f"Creando aeronave con datos: {data}")
        url = f"{self.base_url}{self.aircrafts_endpoint}"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json() if response.content else {}
            validate(instance=response_json, schema=aircraft_out_schema)
            aircraft_id = response_json.get("id")
            if aircraft_id:
                self.created_aircraft_ids.append(aircraft_id)
                logging.info(f"Aeronave creada exitosamente. ID: {aircraft_id}")
            return response.status_code, response_json
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP al crear aeronave. Status: {e.response.status_code} - Body: {e.response.text}")
            return e.response.status_code, {}
        except (json.JSONDecodeError, KeyError) as e:
            logging.error(f"Error al procesar la respuesta JSON: {e}")
            return response.status_code if 'response' in locals() else None, {}
        except ValidationError as e:
            logging.error(f"Error de validación del esquema de la respuesta: {e}")
            return response.status_code if 'response' in locals() else None, {}
        except Exception as e:
            logging.error(f"Error inesperado al crear aeronave: {e}")
            return None, {}

    def get_aircraft_by_id(self, aircraft_id):
        """Obtiene aeronave por ID"""
        url = f"{self.base_url}{self.aircrafts_endpoint}/{aircraft_id}"
        headers = {"Authorization": self.token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP al obtener aeronave por ID: {e}")
            return e.response.status_code, {}
        except Exception as e:
            logging.error(f"Error inesperado al obtener aeronave por ID: {e}")
            return None, {}

    def delete_aircraft(self, aircraft_id):
        """Elimina aeronave por ID"""
        url = f"{self.base_url}{self.aircrafts_endpoint}/{aircraft_id}"
        headers = {"Authorization": self.token}
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            if aircraft_id in self.created_aircraft_ids:
                self.created_aircraft_ids.remove(aircraft_id)
            return response.status_code
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP al eliminar aeronave: {e}")
            return e.response.status_code
        except Exception as e:
            logging.error(f"Error inesperado al eliminar aeronave: {e}")
            return None
