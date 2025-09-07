#Ruta: src/schemas/login_schemas.py
# src/schemas/login_schemas.py
login_response_schema = {
    "title": "LoginResponse",
    "type": "object",
    "properties": {
        "access_token": {"type": "string"},
        "token_type": {"type": "string"}
    },
    "required": ["access_token", "token_type"]
}
