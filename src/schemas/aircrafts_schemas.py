from jsonschema import validate, ValidationError

# aircrafts_schemas.py
aircraft_create_schema = {
    "type": "object",
    "properties": {
        "tail_number": {
            "type": "string",
            "minLength": 5,
            "maxLength": 10
        },
        "model": {
            "type": "string"
        },
        "capacity": {
            "type": "integer"
        }
    },
    "required": ["tail_number", "model", "capacity"]
}

aircraft_out_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "tail_number": {
            "type": "string",
            "minLength": 5,
            "maxLength": 10
        },
        "model": {
            "type": "string"
        },
        "capacity": {
            "type": "integer"
        }
    },
    "required": ["id", "tail_number", "model", "capacity"]
}