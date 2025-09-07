# src/helpers/csv_loader.py

import csv
import os
from typing import List, Dict, Optional


def _resolve_filepath(filename: Optional[str]) -> str:
    """
    Devuelve la ruta absoluta al CSV. Si filename es None, busca data/aircrafts.csv
    relativo al root del proyecto (dos niveles arriba de esta carpeta).
    """
    if filename:
        return filename if os.path.isabs(filename) else os.path.join(os.getcwd(), filename)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(project_root, "data", "aircrafts.csv")


def _parse_row(row: Dict[str, str]) -> Dict[str, object]:
    """
    Normaliza una fila del CSV: trim de strings y conversión segura de capacity a int.
    """
    parsed = {}
    for k, v in row.items():
        if v is None:
            parsed[k] = None
            continue
        value = v.strip()
        if k.lower() == "capacity":
            if value == "":
                parsed[k] = None
            else:
                try:
                    parsed[k] = int(value)
                except ValueError:
                    # Si no se puede convertir, dejamos el valor original (para que el test
                    # pueda verificar comportamiento de la API ante datos mal formados).
                    parsed[k] = value
        else:
            parsed[k] = value
    return parsed


def load_aircrafts_from_csv(filename: Optional[str] = None) -> List[Dict[str, object]]:
    """
    Lee un CSV de aeronaves y devuelve una lista de dicts con claves:
    'tail_number', 'model', 'capacity'.
    - Si filename es None, busca data/aircrafts.csv en la raíz del proyecto.
    - Mantiene capacity como int cuando se puede convertir.
    """
    filepath = _resolve_filepath(filename)
    records: List[Dict[str, object]] = []

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el CSV en la ruta: {filepath}")

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed = _parse_row(row)
            records.append(parsed)

    return records


# alias retrocompatible (si tu código usa otro nombre)
def load_aircrafts_csv(filename: Optional[str] = None) -> List[Dict[str, object]]:
    return load_aircrafts_from_csv(filename)
