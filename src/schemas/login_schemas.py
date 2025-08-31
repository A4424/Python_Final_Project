#Ruta: src/schemas/login_schemas.py

from jsonschema import validate, ValidationError

login_schema = {
    "title": "Body_login_auth_login_post",
    "type": "object",
    "properties": {
        "grant_type": {
            "type": ["string", "null"]
        },
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string"
        },
        "scope": {
            "type": "string"
        },
        "client_id": {
            "type": ["string", "null"]
        },
        "client_secret": {
            "type": ["string", "null"]
        }
    },
    "required": ["username", "password"]
}