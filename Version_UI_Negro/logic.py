"""
logic.py
Reglas de negocio y validaciones.
No sabe nada de UI ni de base de datos.
"""

import re
from datetime import datetime
import models
import database


# ── Validaciones de campos ────────────────────────────────────

def validar_name(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "Name ist ein Pflichtfeld."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "Name: nur Buchstaben erlaubt."
    return True, ""


def validar_vorname(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "Vorname ist ein Pflichtfeld."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "Vorname: nur Buchstaben erlaubt."
    return True, ""


def validar_gebdatum(valor: str) -> tuple[bool, str]:
    valor = valor.strip().replace(",", ".")
    if not valor:
        return False, "Geburtsdatum ist ein Pflichtfeld."
    patron = r"^\d{2}\.\d{2}\.\d{4}$"
    if not re.match(patron, valor):
        return False, "Geburtsdatum: bitte Format DD.MM.YYYY verwenden."
    try:
        fecha = datetime.strptime(valor, "%d.%m.%Y")
    except ValueError:
        return False, "Geburtsdatum: ungültiger Tag oder Monat."
    if fecha > datetime.now() or fecha.year < 1900:
        return False, "Geburtsdatum: bitte ein gültiges Jahr eingeben (1900 – heute)."
    return True, ""


def validar_telefono(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if valor == "":
        return True, ""
    if not re.match(r"^[\d\s\+\-\(\)]{6,20}$", valor):
        return False, "Telefon: nur Ziffern, +, - erlaubt. z.B. +49 30 123456"
    return True, ""


def validar_email(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if valor == "":
        return True, ""
    if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", valor):
        return False, "E-Mail ungültig. z.B. beispiel@mail.com"
    return True, ""


def validar_direccion(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if valor == "":
        return True, ""
    tiene_letra  = any(c.isalpha() for c in valor)
    tiene_numero = any(c.isdigit() for c in valor)
    if not (tiene_letra and tiene_numero):
        return False, "Adresse: Straße und Nr. angeben. z.B. Boddinstr. 10"
    return True, ""


def validar_obligatorios(vals: dict) -> tuple[bool, str]:
    obligatorios = {"name": "Name", "vorname": "Vorname", "gebdatum": "Geburtsdatum"}
    faltantes = [etiqueta for key, etiqueta in obligatorios.items()
                 if not vals.get(key, "").strip()]
    if faltantes:
        return False, f"Pflichtfelder ausfüllen: {', '.join(faltantes)}"
    return True, ""


def validar_todos(vals: dict) -> tuple[bool, str]:
    ok, msg = validar_obligatorios(vals)
    if not ok:
        return False, msg
    checks = [
        validar_name(vals["name"]),
        validar_vorname(vals["vorname"]),
        validar_gebdatum(vals["gebdatum"]),
        validar_telefono(vals.get("telefono", "")),
        validar_email(vals.get("email", "")),
        validar_direccion(vals.get("direccion", "")),
    ]
    for ok, msg in checks:
        if not ok:
            return False, msg
    return True, ""


# ── Operaciones sobre pacientes ───────────────────────────────

def fecha_hoy() -> str:
    return datetime.now().strftime("%d.%m.%Y")


def crear_patient(name, vorname, gebdatum,
                  telefono="", email="", direccion="") -> models.Person:
    p = models.Person(
        name         = name.strip().title(),
        vorname      = vorname.strip().title(),
        gebdatum     = gebdatum.strip(),
        systemzugang = fecha_hoy(),
        telefono     = telefono.strip(),
        email        = email.strip(),
        direccion    = direccion.strip(),
    )
    database.guardar(p)
    return p


def actualizar_patient(patient: models.Person, vals: dict) -> None:
    patient.set_name(vals["name"].strip().title())
    patient.set_vorname(vals["vorname"].strip().title())
    patient.set_gebdatum(vals["gebdatum"].strip())
    patient.set_telefono(vals.get("telefono", "").strip())
    patient.set_email(vals.get("email", "").strip())
    patient.set_direccion(vals.get("direccion", "").strip())
    database.actualizar(patient)


def buscar_patients(name: str) -> list[models.Person]:
    return database.buscar(name.strip().title())


def borrar_patient(patient: models.Person, lista: list) -> None:
    database.borrar(patient.get_id())
    lista.remove(patient)
