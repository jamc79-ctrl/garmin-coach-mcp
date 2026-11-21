from __future__ import annotations

import getpass
import os
from pathlib import Path

import env_loader  # noqa: F401  (carga garmin.env)
from garminconnect import Garmin


def main() -> None:
    # Si rellenaste garmin.env se usan esos valores; si no, se piden aquí.
    email = os.getenv("GARMIN_EMAIL", "").strip() or input("Email Garmin: ").strip()
    password = os.getenv("GARMIN_PASSWORD", "") or getpass.getpass("Contraseña Garmin: ")

    token_dir = Path.home() / ".garminconnect"
    token_dir.mkdir(parents=True, exist_ok=True)

    client = Garmin(
        email=email,
        password=password,
        prompt_mfa=lambda: input("Código MFA que te llegue por email: ").strip(),
    )

    client.login(str(token_dir))

    token_file = token_dir / "garmin_tokens.json"
    print("\nLogin OK.")
    print(f"Archivo de tokens: {token_file}\n")
    print("Pega este JSON entero en Railway como GARMIN_TOKENS_JSON:\n")
    print(token_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
