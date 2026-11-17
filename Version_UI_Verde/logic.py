# logic.py
from datetime import datetime
import patient_klasse
import adresse_klasse
import verschreibung_klasse
import datenbank
import re

# Validaciones — devuelven (bool, str)
# True  → (True,  valor_limpio)
# False → (False, mensaje_de_error)

# ─── Validaciones Patient ─────────────────────────────────────

def name_eingabe(name: str) -> tuple[bool, str]:
    valor = name.strip()
    if not valor:
        return False, "Name ist ein Pflichtfeld."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "Name: \nNur Buchstaben erlaubt."
    return True, valor

def vorname_eingabe(vorname: str) -> tuple[bool, str]:
    valor = vorname.strip()
    if not valor:
        return False, "Vorname ist ein Pflichtfeld."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "Vorname:\nNur Buchstaben erlaubt."
    return True, valor

def gebdatum_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip().replace(",", ".").replace("/", ".").replace("-", ".")
    if not valor:
        return False, "Geburtsdatum ist \nein Pflichtfeld."
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", valor):
        return False, "Geburtsdatum Bitte Format \nDD.MM.YYYY verwenden."
    try:
        fecha = datetime.strptime(valor, "%d.%m.%Y")
    except ValueError:
        return False, "Ungültiger Tag \noder Monat."
    if fecha > datetime.now() or fecha.year < 1900:
        return False, "Geburtsdatum Bitte ein gültiges \nJahr eingeben (1900 – heute)."
    return True, valor

def systemzugang() -> str:
    return datetime.now().strftime("%d.%m.%Y")

def telefon_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if valor == "":
        return True, ""
    if not re.match(r"^[\d\s\+\-\(\)]{6,20}$", valor):
        return False, "Telefon: Nur Ziffern, + and -\nerlaubt z.B. +49 30 123456"
    return True, valor

def email_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if valor == "":
        return True, ""
    if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", valor):
        return False, "E-Mail ungültig. \nz.B. beispiel@mail.com"
    return True, valor


# ─── Validaciones Adresse ─────────────────────────────────────

def strasse_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "Straße ist \nein Pflichtfeld."
    if not any(c.isalpha() for c in valor):
        return False, "Straße: Nur Text erlaubt.\nz.B. Boddinstraße"
    return True, valor

def hausnummer_eingabe(valor: str) -> tuple[bool, str]:
    if not valor:
        return False, "Hausnummer ist \nein Pflichtfeld."
    if not re.match(r"^\d+[a-zA-Z]?$", valor):
        return False, "Hausnummer ungültig.\nz.B. 10 oder 10a"
    return True, valor

def plz_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "PLZ ist \nein Pflichtfeld."
    if not re.match(r"^\d{5}$", valor):
        return False, "PLZ: 5 Ziffern.\nz.B. 12345"
    return True, valor

def ort_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "Ort ist \nein Pflichtfeld."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "Ort: Nur Buchstaben erlaubt.\nz.B. Berlin"
    return True, valor


# ─── Validaciones Verschreibung ───────────────────────────────

def frequenz_eingabe(valor: str) -> tuple[bool, str]:
    valor = valor.strip()
    if not valor:
        return False, "Frequenz ist ein Pflichtfeld."
    return True, valor

def datum_eingabe(valor: str) -> tuple[bool, str]:
    # mismo patrón que gebdatum pero sin restricción de fecha futura
    # el datum de una prescripción puede ser hoy o en el futuro
    valor = valor.strip().replace(",", ".").replace("/", ".").replace("-", ".")
    if not valor:
        return False, "Datum ist ein Pflichtfeld."
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", valor):
        return False, "Datum: Format \nDD.MM.YYYY verwenden."
    try:
        datetime.strptime(valor, "%d.%m.%Y")
    except ValueError:
        return False, "Ungültiger Tag \noder Monat."
    return True, valor


# ─── Patient CRUD ─────────────────────────────────────────────

def patient_neu(name, vorname, gebdatum, systemzugang, telefon="", email="") -> patient_klasse.Patient | None:
    name         = name.strip().title()
    vorname      = vorname.strip().title()
    gebdatum     = gebdatum.strip()
    systemzugang = systemzugang.strip()
    telefon      = telefon.strip()
    email        = email.strip()

    if datenbank.vermeiden_duplicat(name, vorname, gebdatum, systemzugang, telefon, email):
        return None  # duplicado — no guardamos

    neues_patient_obj = patient_klasse.Patient(
        name         = name,
        vorname      = vorname,
        gebdatum     = gebdatum,
        systemzugang = systemzugang,
        telefon      = telefon,
        email        = email
    )
    datenbank.patient_save(neues_patient_obj)
    return neues_patient_obj

def patient_delete(patient: patient_klasse.Patient, lista: list) -> None:
    # 1 — borra la dirección vinculada
    aid = patient.get_adresse_id()
    if aid:
        datenbank.adresse_delete(aid)
    # 2 — borra todas las prescripciones vinculadas
    for vid in patient.get_verschreibung_ids():
        datenbank.verschreibung_delete(vid)
    # 3 — borra al paciente
    datenbank.patient_delete(patient.get_id())
    lista.remove(patient)

def patient_bearbeiten(patient: patient_klasse.Patient, name, vorname, gebdatum, systemzugang, telefon, email) -> None:
    patient.set_name(name.strip().title())
    patient.set_vorname(vorname.strip().title())
    patient.set_gebdatum(gebdatum.strip())
    patient.set_systemzugang(systemzugang.strip())
    patient.set_telefon(telefon.strip())
    patient.set_email(email.strip())
    datenbank.patient_bearbeiten(patient)


# ─── Adresse CRUD ─────────────────────────────────────────────

def adresse_neu(patient: patient_klasse.Patient, strasse, hausnummer, plz, ort) -> adresse_klasse.Adresse:
    nueva = adresse_klasse.Adresse(
        strasse    = strasse.strip().title(),
        hausnummer = hausnummer.strip(),
        plz        = plz.strip(),
        ort        = ort.strip().title(),
    )
    nueva = datenbank.adresse_save(nueva)                       # asigna AID
    datenbank.adresse_verknuepfen(patient, nueva.get_adresseID()) # vincula al paciente
    return nueva

def adresse_bearbeiten(adresse: adresse_klasse.Adresse, strasse, hausnummer, plz, ort) -> None:
    adresse.set_strasse(strasse.strip().title())
    adresse.set_hausnummer(hausnummer.strip())
    adresse.set_plz(plz.strip())
    adresse.set_ort(ort.strip().title())
    datenbank.adresse_bearbeiten(adresse)

def adresse_delete(patient: patient_klasse.Patient, adresse: adresse_klasse.Adresse) -> None:
    datenbank.adresse_entknuepfen(patient)
    datenbank.adresse_delete(adresse.get_adresseID())

def patient_adresse_load(patient: patient_klasse.Patient):
    return datenbank.adresse_load_von_patient(patient.get_adresse_id())


# ─── Verschreibung CRUD ───────────────────────────────────────
# mismo patrón que Adresse CRUD

def verschreibung_neu(patient: patient_klasse.Patient, medikamentID: str, frequenz: str, datum: str) -> verschreibung_klasse.Verschreibung:
    nueva = verschreibung_klasse.Verschreibung(
        medikamentID = medikamentID,
        frequenz     = frequenz.strip(),
        datum        = datum.strip(),
    )
    nueva = datenbank.verschreibung_save(nueva)                              # asigna VID
    datenbank.verschreibung_verknuepfen(patient, nueva.get_verschreibungID())  # vincula al paciente
    return nueva

def verschreibung_delete(patient: patient_klasse.Patient, verschreibung: verschreibung_klasse.Verschreibung) -> None:
    datenbank.verschreibung_entknuepfen(patient, verschreibung.get_verschreibungID())
    datenbank.verschreibung_delete(verschreibung.get_verschreibungID())

def patient_verschreibungen_load(patient: patient_klasse.Patient) -> list:
    # devuelve los objetos Verschreibung del paciente
    # mismo puente que patient_adressen_load
    return datenbank.verschreibung_load_von_patient(patient.get_verschreibung_ids())
