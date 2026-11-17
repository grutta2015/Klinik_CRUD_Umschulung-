# datenbank.py
import pickle
import os
import patient_klasse

ARCHIVO               = "patienten"       # objetos Patient
ARCHIVO_ADRESSEN      = "adressen"        # objetos Adresse
ARCHIVO_VADEMECUM     = "vademecum"       # objetos Medikamente (catálogo)
ARCHIVO_VERSCHREIBUNG = "verschreibungen" # objetos Verschreibung (prescripciones por paciente)

# Patrón general de todas las operaciones:
# leer lista → modificar lista → escribir lista

def inicializar():
    print("\nDatenbank initialisiert.")

def cerrar():
    print("\nDatenbank geschlossen.")


# ─── PATIENTEN ────────────────────────────────────────────────────────────────

def _patienten_load_list():
    if not os.path.exists(ARCHIVO):
        return []
    datei = open(ARCHIVO, 'rb')
    patienten = pickle.load(datei)
    datei.close()
    return patienten

def _patienten_write_list(patienten):
    datei = open(ARCHIVO, 'wb')
    pickle.dump(patienten, datei)
    datei.close()

def vermeiden_duplicat(name, vorname, gebdatum, systemzugang, telefon, email):
    patienten = _patienten_load_list()
    for p in patienten:
        if (p.get_name() == name and p.get_vorname() == vorname and p.get_gebdatum() == gebdatum and
            p.get_systemzugang() == systemzugang and p.get_telefon() == telefon and p.get_email() == email):
            return True
    return False

def patient_save(patient):
    patienten = _patienten_load_list()
    if patienten:
        ultimo_id = patienten[-1].get_id()   # ej: "PID0007"
        numero = int(ultimo_id[3:]) + 1
    else:
        numero = 1
    patient.set_id(f"PID{numero:04d}")
    patienten.append(patient)
    _patienten_write_list(patienten)

def patient_load():
    return _patienten_load_list()

def patient_delete(id):
    patienten = _patienten_load_list()
    neues_list = [p for p in patienten if p.get_id() != id]
    _patienten_write_list(neues_list)

def patient_bearbeiten(patient):
    patienten = _patienten_load_list()
    neues_list = []
    for p in patienten:
        if p.get_id() == patient.get_id():
            neues_list.append(patient)   # versión nueva
        else:
            neues_list.append(p)
    _patienten_write_list(neues_list)


# ─── ADRESSEN ─────────────────────────────────────────────────────────────────

def _adressen_load_list():
    if not os.path.exists(ARCHIVO_ADRESSEN):
        return []
    datei = open(ARCHIVO_ADRESSEN, 'rb')
    adressen = pickle.load(datei)
    datei.close()
    return adressen

def _adressen_write_list(adressen):
    datei = open(ARCHIVO_ADRESSEN, 'wb')
    pickle.dump(adressen, datei)
    datei.close()

def adresse_save(adresse):
    adressen = _adressen_load_list()
    if adressen:
        ultimo_id = adressen[-1].get_adresseID()  # ej: "AID0007"
        numero = int(ultimo_id[3:]) + 1
    else:
        numero = 1
    adresse.set_adresseID(f"AID{numero:04d}")
    adressen.append(adresse)
    _adressen_write_list(adressen)
    return adresse   # devuelve el objeto con AID asignado — logic.py lo necesita

def adresse_load():
    return _adressen_load_list()

def adresse_load_von_patient(adresse_id: str):
    # recibe un AID y devuelve el objeto Adresse correspondiente
    adressen = _adressen_load_list()
    for a in adressen:
        if a.get_adresseID() == adresse_id:
            return a
    return None

def adresse_delete(adresseID):
    adressen = _adressen_load_list()
    neues_list = [a for a in adressen if a.get_adresseID() != adresseID]
    _adressen_write_list(neues_list)

def adresse_bearbeiten(adresse):
    adressen = _adressen_load_list()
    neues_list = []
    for a in adressen:
        if a.get_adresseID() == adresse.get_adresseID():
            neues_list.append(adresse)
        else:
            neues_list.append(a)
    _adressen_write_list(neues_list)

# ─── VINKULIERUNG Patient ↔ Adresse ───────────────────────────────────────────

def adresse_verknuepfen(patient, adresseID: str):
    # asigna el AID al paciente y guarda
    patient.set_adresse_id(adresseID)
    patient_bearbeiten(patient)

def adresse_entknuepfen(patient):
    # quita el AID del paciente y guarda
    patient.set_adresse_id(None)
    patient_bearbeiten(patient)


# ─── VADEMECUM ────────────────────────────────────────────────────────────────
# Catálogo de medicamentos disponibles — objetos Medikamente
# Solo se lee para mostrar en la UI — el guardado lo hace el administrador del sistema

def _vademecum_load_list():
    if not os.path.exists(ARCHIVO_VADEMECUM):
        return []
    datei = open(ARCHIVO_VADEMECUM, 'rb')
    vademecum = pickle.load(datei)
    datei.close()
    return vademecum

def _vademecum_write_list(vademecum):
    datei = open(ARCHIVO_VADEMECUM, 'wb')
    pickle.dump(vademecum, datei)
    datei.close()

def vademecum_load_list():
    # función pública — la llama ui_controller.py para cargar el catálogo
    return _vademecum_load_list()

def vademecum_save(medikament):
    # guarda un medicamento nuevo en el catálogo y le asigna su MID
    vademecum = _vademecum_load_list()
    if vademecum:
        ultimo_id = vademecum[-1].get_medikamentID()  # ej: "MID0007"
        numero = int(ultimo_id[3:]) + 1
    else:
        numero = 1
    medikament.set_medikamentID(f"MID{numero:04d}")
    vademecum.append(medikament)
    _vademecum_write_list(vademecum)
    return medikament


# ─── VERSCHREIBUNGEN ──────────────────────────────────────────────────────────
# Prescripciones — unen un medicamento del vademecum con un paciente
# Mismo patrón exacto que Adressen

def _verschreibung_load_list():
    if not os.path.exists(ARCHIVO_VERSCHREIBUNG):
        return []
    datei = open(ARCHIVO_VERSCHREIBUNG, 'rb')
    verschreibungen = pickle.load(datei)
    datei.close()
    return verschreibungen

def _verschreibung_write_list(verschreibungen):
    datei = open(ARCHIVO_VERSCHREIBUNG, 'wb')
    pickle.dump(verschreibungen, datei)
    datei.close()

def verschreibung_save(verschreibung):
    # guarda la prescripción y le asigna su VID — devuelve el objeto con VID asignado
    verschreibungen = _verschreibung_load_list()
    if verschreibungen:
        ultimo_id = verschreibungen[-1].get_verschreibungID()  # ej: "VID0007"
        numero = int(ultimo_id[3:]) + 1
    else:
        numero = 1
    verschreibung.set_verschreibungID(f"VID{numero:04d}")
    verschreibungen.append(verschreibung)
    _verschreibung_write_list(verschreibungen)
    return verschreibung   # devuelve objeto con VID — logic.py lo necesita para vincular

def verschreibung_load_von_patient(verschreibung_ids: list):
    # recibe lista de VIDs del paciente y devuelve los objetos Verschreibung
    # es el mismo puente que adresse_load_von_patient
    verschreibungen = _verschreibung_load_list()
    return [v for v in verschreibungen if v.get_verschreibungID() in verschreibung_ids]

def verschreibung_delete(verschreibungID: str):
    # mismo patrón que adresse_delete
    verschreibungen = _verschreibung_load_list()
    neues_list = [v for v in verschreibungen if v.get_verschreibungID() != verschreibungID]
    _verschreibung_write_list(neues_list)

# ─── VINKULIERUNG Patient ↔ Verschreibung ─────────────────────────────────────

def verschreibung_verknuepfen(patient, verschreibungID: str):
    # agrega VID a la lista del paciente y guarda
    patient.add_verschreibung_id(verschreibungID)
    patient_bearbeiten(patient)

def verschreibung_entknuepfen(patient, verschreibungID: str):
    # quita VID de la lista del paciente y guarda
    patient.remove_verschreibung_id(verschreibungID)
    patient_bearbeiten(patient)
