# ui_controller.py
import logic
import datenbank
import config
from tkinter import messagebox

# ─── Estado global ────────────────────────────────────────────
gui             = {}                  # widgets inyectados desde ui.py
_p              = config.get_palette()
alle_patienten  = datenbank.patient_load()
current_index   = [0]
adresse_actual  = None

# ─── Helpers internos ─────────────────────────────────────────

def _set_field(key, valor):
    """Limpia el entry y escribe un valor."""
    gui[key].delete(0, "end")
    gui[key].insert(0, valor)

def _error(msg, ok=False):
    """Muestra mensaje en el label de error (rojo) o confirmación (verde)."""
    color = _p["BESTAETIGUNG_FARBE"] if ok else _p["FEHLER_FARBE"]
    gui["error_label"].configure(text=msg, text_color=color)

def _validar_campos_gui() -> tuple[bool, dict]:
    """Valida todos los campos del formulario. Devuelve (True, valores) o (False, {})."""
    campos = [
        ("name",       logic.name_eingabe),
        ("vorname",    logic.vorname_eingabe),
        ("geburt",     logic.gebdatum_eingabe),
        ("telefon",    logic.telefon_eingabe),
        ("email",      logic.email_eingabe),
        ("strasse",    logic.strasse_eingabe),
        ("hausnummer", logic.hausnummer_eingabe),
        ("plz",        logic.plz_eingabe),
        ("ort",        logic.ort_eingabe),
    ]
    valores = {}
    for key, validar in campos:
        ok, msg = validar(gui[key].get())
        if not ok:
            _error(msg)
            return False, {}
        valores[key] = msg
    return True, valores

def _solo_abrir_ventana():
    # placeholder — se conecta cuando se implemente "Ver Recetado"
    pass


# ─── Patient: mostrar / limpiar ───────────────────────────────

def mostrar_patient(index):
    """Carga los datos del paciente[index] en la GUI."""
    if not alle_patienten:
        return
    p = alle_patienten[index]

    _set_field("name",    p.get_name())
    _set_field("vorname", p.get_vorname())
    _set_field("geburt",  p.get_gebdatum())
    _set_field("telefon", p.get_telefon())
    _set_field("email",   p.get_email())

    gui["id_label"].configure(text=f"ID: {p.get_id()}")
    _error("")

    # Carga la dirección del paciente
    global adresse_actual
    adresse_actual = logic.patient_adresse_load(p)
    if adresse_actual:
        _mostrar_adresse()
    else:
        _limpiar_campos_adresse()

    campos_a_bloquear = ["name", "vorname", "geburt", "telefon", "email", "strasse"]
    for clave in campos_a_bloquear:
        gui[clave].configure(state="readonly")

def limpiar_campos():
    """Vacía todos los campos (paciente + adresse) para un registro nuevo."""
    for key in ["name", "vorname", "telefon", "email"]:
        gui[key].delete(0, "end")
    _set_field("geburt", config.GEBDATUM_HINT)
    gui["id_label"].configure(text="ID: —")
    _error("")
    _limpiar_campos_adresse()


# ─── Patient: CRUD ────────────────────────────────────────────

def speichern():
    """Valida, crea el paciente y su primera dirección, y los guarda."""
    ok, v = _validar_campos_gui()
    if not ok:
        return

    nuevo = logic.patient_neu(
        v["name"], v["vorname"], v["geburt"],
        logic.systemzugang(),
        v["telefon"], v["email"]
    )

    if nuevo is None:
        _error("Patient bereits vorhanden.")
        return

    logic.adresse_neu(nuevo, v["strasse"], v["hausnummer"], v["plz"], v["ort"])

    alle_patienten.append(nuevo)
    current_index[0] = len(alle_patienten) - 1
    mostrar_patient(current_index[0])
    _error("✓ Patient gespeichert", ok=True)

def bearbeiten():
    if not alle_patienten:
        return
    patient = alle_patienten[current_index[0]]

    campos_patient = [
        ("name",       logic.name_eingabe),
        ("vorname",    logic.vorname_eingabe),
        ("geburt",     logic.gebdatum_eingabe),
        ("telefon",    logic.telefon_eingabe),
        ("email",      logic.email_eingabe),
        ("strasse",    logic.strasse_eingabe),
        ("hausnummer", logic.hausnummer_eingabe),
        ("plz",        logic.plz_eingabe),
        ("ort",        logic.ort_eingabe),
    ]
    v = {}
    for key, validar in campos_patient:
        ok, msg = validar(gui[key].get())
        if not ok:
            _error(msg)
            return
        v[key] = msg

    logic.patient_bearbeiten(
        patient,
        v["name"], v["vorname"], v["geburt"],
        patient.get_systemzugang(),
        v["telefon"], v["email"]
    )

    if adresse_actual:
        logic.adresse_bearbeiten(adresse_actual, v["strasse"], v["hausnummer"], v["plz"], v["ort"])

    _error("✓ Aktualisiert", ok=True)

def delete():
    """Borra al paciente actual tras confirmación."""
    if not alle_patienten:
        return
    p = alle_patienten[current_index[0]]
    if messagebox.askyesno("Löschen", f"Patient {p.get_name()} löschen?"):
        logic.patient_delete(p, alle_patienten)
    limpiar_campos()
    _error("✓ Patient gelöscht", ok=True)

def prev_patient():
    if not alle_patienten: return
    current_index[0] = (current_index[0] - 1) % len(alle_patienten)
    mostrar_patient(current_index[0])

def next_patient():
    if not alle_patienten: return
    current_index[0] = (current_index[0] + 1) % len(alle_patienten)
    mostrar_patient(current_index[0])

def filtrar_list_busqueda_dinamica(texto):
    resultado = []
    for p in alle_patienten:
        if texto in p.get_name().lower() or texto in p.get_vorname().lower():
            a = logic.patient_adresse_load(p)
            resultado.append((p, a))
    return resultado


# ─── Adresse: mostrar / limpiar ───────────────────────────────

def _mostrar_adresse():
    if not adresse_actual: return
    a = adresse_actual
    _set_field("strasse",    a.get_strasse())
    _set_field("hausnummer", a.get_hausnummer())
    _set_field("plz",        a.get_plz())
    _set_field("ort",        a.get_ort())
    gui["id_adresse"].configure(text=f"AID: {a.get_adresseID()}")

    campos_a_bloquear = ["strasse", "hausnummer", "plz", "ort"]
    for clave in campos_a_bloquear:
        gui[clave].configure(state="readonly")

def _limpiar_campos_adresse():
    for key in ["strasse", "hausnummer", "plz", "ort"]:
        gui[key].delete(0, "end")
    gui["id_adresse"].configure(text="AID: —")


# ─── Adresse: CRUD ────────────────────────────────────────────

def speichern_adresse():
    """Valida y guarda la dirección vinculada al paciente actual."""
    if not alle_patienten:
        return
    patient = alle_patienten[current_index[0]]

    campos_adresse = [
        ("strasse",    logic.strasse_eingabe),
        ("hausnummer", logic.hausnummer_eingabe),
        ("plz",        logic.plz_eingabe),
        ("ort",        logic.ort_eingabe),
    ]
    v = {}
    for key, validar in campos_adresse:
        ok, msg = validar(gui[key].get())
        if not ok:
            _error(msg)
            return
        v[key] = msg

    global adresse_actual
    adresse_actual = logic.adresse_neu(patient, v["strasse"], v["hausnummer"], v["plz"], v["ort"])
    _mostrar_adresse()
    _error("✓ Adresse gespeichert", ok=True)


# ─── Vademecum: buscar ────────────────────────────────────────

def filtrar_list_busqueda_vademecum(texto):
    # filtra el catálogo de medicamentos por nombre
    texto = texto.lower()
    resultado = []
    for m in datenbank.vademecum_load_list():
        if texto in m.get_name().lower():
            resultado.append(m)
    return resultado


# ─── Verschreibung: guardar / cargar ─────────────────────────

def verschreibung_speichern(medikament, frequenz: str, datum: str):
    """
    Recibe el objeto Medikamente seleccionado del vademecum, la frequenz y el datum.
    Toma el paciente actual desde el estado global (current_index).
    Crea y guarda la prescripción vinculada al paciente.
    """
    if not alle_patienten:
        return False, "Kein Patient ausgewählt."

    # valida los campos antes de guardar
    ok_f, frequenz = logic.frequenz_eingabe(frequenz)
    if not ok_f:
        return False, frequenz   # devuelve el mensaje de error

    ok_d, datum = logic.datum_eingabe(datum)
    if not ok_d:
        return False, datum

    patient = alle_patienten[current_index[0]]

    # crea la prescripción con el MID del medicamento del vademecum
    logic.verschreibung_neu(patient, medikament.get_medikamentID(), frequenz, datum)

    return True, "✓ Medikament verschrieben"

def verschreibung_delete_von_patient(verschreibung):
    """Borra una prescripción del paciente actual."""
    if not alle_patienten:
        return
    patient = alle_patienten[current_index[0]]
    logic.verschreibung_delete(patient, verschreibung)

def patient_verschreibungen_load():
    """Devuelve las prescripciones del paciente actual como lista de objetos Verschreibung."""
    if not alle_patienten:
        return []
    patient = alle_patienten[current_index[0]]
    return logic.patient_verschreibungen_load(patient)

def vademecum_get_by_id(medikamentID: str):
    """
    Dado un MID, devuelve el objeto Medikamente del vademecum.
    Útil para mostrar el nombre del medicamento en la ventana 'Ver Recetado'.
    """
    for m in datenbank.vademecum_load_list():
        if m.get_medikamentID() == medikamentID:
            return m
    return None   # no encontrado — no debería pasar si los datos son consistentes
