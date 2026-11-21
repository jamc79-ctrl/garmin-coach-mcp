"""Carga variables desde garmin.env (si existe) antes de que el servidor lea el entorno.

- Busca garmin.env junto a este archivo, o en la ruta indicada en GARMIN_ENV_FILE.
- Formato: CLAVE=valor por línea; ignora líneas vacías y comentarios (#).
- No pisa variables que ya existan en el entorno (Railway, shell, etc.).
- Sin dependencias externas.
"""
from __future__ import annotations

import os
from pathlib import Path


def load_garmin_env() -> Path | None:
    custom = os.getenv("GARMIN_ENV_FILE", "").strip()
    path = Path(custom).expanduser() if custom else Path(__file__).resolve().parent / "garmin.env"
    if not path.is_file():
        return None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if key and value and key not in os.environ:
            os.environ[key] = value
    return path


load_garmin_env()
