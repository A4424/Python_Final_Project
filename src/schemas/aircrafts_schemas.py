# # Ruta: src/schemas/aircrafts_schemas.py
# from jsonschema import validate
#
# # -------------------------------
# # Schema de creación de aeronave
# # -------------------------------
# aircraft_create_schema = {
#     "title": "Body_aircraft_create",
#     "type": "object",
#     "properties": {
#         "model": {"type": "string"},
#         "capacity": {"type": "integer"},
#         "tail_number": {"type": "string"}
#     },
#     "required": ["model", "capacity", "tail_number"],
#     "additionalProperties": False
# }
#
# # -------------------------------
# # Schema de salida de aeronave
# # -------------------------------
# aircraft_out_schema = {
#     "title": "Body_aircraft_out",
#     "type": "object",
#     "properties": {
#         "id": {"type": "string"},
#         "model": {"type": "string"},
#         "capacity": {"type": "integer"},
#         "tail_number": {"type": "string"}
#     },
#     "required": ["id", "model", "capacity", "tail_number"],
#     "additionalProperties": False
# }
#
# # -------------------------------
# # Schema de actualización de aeronave
# # -------------------------------
# # Permite "id" en la respuesta para cumplir con lo que devuelve el backend
# aircraft_update_schema = {
#     "title": "Body_aircraft_update",
#     "type": "object",
#     "properties": {
#         "id": {"type": "string"},  # agregado para no fallar jsonschema
#         "model": {"type": "string"},
#         "capacity": {"type": "integer"},
#         "tail_number": {"type": "string"}
#     },
#     "required": ["model", "capacity", "tail_number"],
#     "additionalProperties": False
# }
#
# # -------------------------------
# # Schema de errores (422 o 500)
# # -------------------------------
# aircraft_error_schema = {
#     "title": "Body_aircraft_error",
#     "type": "object",
#     "properties": {
#         "detail": {"type": "string"},
#         "message": {"type": "string"}
#     },
#     "additionalProperties": True  # permite campos opcionales del backend
# }
# src/schemas/aircrafts_schemas.py

# Schema para el payload de creación/actualización
aircraft_create_schema = {
    "type": "object",
    "properties": {
        "tail_number": {"type": "string", "minLength": 5, "maxLength": 10},
        "model": {"type": "string"},
        "capacity": {"type": "integer", "minimum": 1}
    },
    "required": ["tail_number", "model", "capacity"],
    "additionalProperties": False
}

# Schema esperado en la respuesta de un recurso Aircraft
aircraft_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": ["integer", "string"]},
        "tail_number": {"type": "string"},
        "model": {"type": "string"},
        "capacity": {"type": "integer"}
    },
    "required": ["id", "tail_number", "model", "capacity"]
}

# Lista de aeronaves (array de objetos)
aircraft_list_schema = {
    "type": "array",
    "items": aircraft_response_schema
}
