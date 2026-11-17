import sqlite3
import models

conn = None


def inicializar():
    global conn
    conn = sqlite3.connect("klinik.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patienten (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            vorname     TEXT,
            gebdatum    TEXT,
            systemzugang TEXT,
            telefono    TEXT DEFAULT '',
            email       TEXT DEFAULT '',
            direccion   TEXT DEFAULT ''
        )
    """)
    # Migración suave: agrega las columnas nuevas si la tabla ya existía sin ellas
    for col in ("telefono", "email", "direccion"):
        try:
            cursor.execute(f"ALTER TABLE patienten ADD COLUMN {col} TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass  # la columna ya existe, no pasa nada
    conn.commit()


def cerrar():
    global conn
    if conn:
        conn.close()


def guardar(patient):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patienten (name, vorname, gebdatum, systemzugang, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient.get_name(),
        patient.get_vorname(),
        patient.get_gebdatum(),
        patient.get_systemzugang(),
        patient.get_telefono(),
        patient.get_email(),
        patient.get_direccion(),
    ))
    conn.commit()
    patient.set_id(cursor.lastrowid)


def load():
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, vorname, gebdatum, systemzugang, telefono, email, direccion FROM patienten")
    patienten = []
    for fila in cursor.fetchall():
        p = models.Person(
            id          = fila[0],
            name        = fila[1],
            vorname     = fila[2],
            gebdatum    = fila[3],
            systemzugang= fila[4],
            telefono    = fila[5],
            email       = fila[6],
            direccion   = fila[7],
        )
        patienten.append(p)
    return patienten


def buscar(name):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, vorname, gebdatum, systemzugang, telefono, email, direccion "
        "FROM patienten WHERE name = ?", (name,)
    )
    patienten = []
    for fila in cursor.fetchall():
        p = models.Person(
            id          = fila[0],
            name        = fila[1],
            vorname     = fila[2],
            gebdatum    = fila[3],
            systemzugang= fila[4],
            telefono    = fila[5],
            email       = fila[6],
            direccion   = fila[7],
        )
        patienten.append(p)
    return patienten


def borrar(id):
    """Elimina un paciente por ID. Solo se llama DESPUÉS de confirmar."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patienten WHERE id = ?", (id,))
    conn.commit()


def actualizar(patient):
    """Actualiza todos los campos de un paciente existente."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patienten
        SET name=?, vorname=?, gebdatum=?, systemzugang=?, telefono=?, email=?, direccion=?
        WHERE id=?
    """, (
        patient.get_name(),
        patient.get_vorname(),
        patient.get_gebdatum(),
        patient.get_systemzugang(),
        patient.get_telefono(),
        patient.get_email(),
        patient.get_direccion(),
        patient.get_id(),
    ))
    conn.commit()
