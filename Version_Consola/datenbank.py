import sqlite3
import meineklasse

conn = None  # variable del módulo, accesible por todas las funcionesbreviatura de connection 
             #—  es la convención universal.

def inicializar():
    global conn
    conn = sqlite3.connect("klinik.db")  # abre o crea el archivo
    cursor = conn.cursor()              #el "lápiz" que ejecuta las instrucciones SQL. conn es la conexión, 
                                        #pero no puede ejecutar SQL directamente — necesitas un cursor para eso.
                                        #  abrir un libro (conn) y tener el dedo 
                                        # con el que señalas las líneas (cursor).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patienten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            vorname TEXT,
            gebdatum TEXT,
            systemzugang TEXT
        )
    """)
    conn.commit()  # confirma y escribe los cambios en el archivo .db. Piénsalo así:
                   # cursor.execute() → prepara el cambio en memoria
                   # conn.commit() → lo graba definitivamente en disco


def cerrar():
    global conn
    if conn:
        conn.close()


def guardar(patient):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patienten (name, vorname, gebdatum, systemzugang)
        VALUES (?, ?, ?, ?)
    """, (patient.get_name(), patient.get_vorname(), patient.get_gebdatum(), patient.get_systemzugang()))
    conn.commit()
    patient.set_id(cursor.lastrowid)  # SQLite devuelve el id generado
                                      #El lastrowid se lee después del commit porque solo en ese momento 
                                      # SQLite ha procesado el INSERT y tiene el ID listo.
def load():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patienten")
    filas = cursor.fetchall()  # lista de tuplas con todos los pacientes
    patienten = []
    for fila in filas:
        # fila = (id, name, vorname, gebdatum, systemzugang)
        p = meineklasse.Person(fila[1], fila[2], fila[3], fila[4], fila[0])
        patienten.append(p)
    return patienten



def buscar(name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patienten WHERE name = ?", (name,))
    filas = cursor.fetchall()
    patienten = []
    for fila in filas:
        p = meineklasse.Person(fila[1], fila[2], fila[3], fila[4], fila[0])
        patienten.append(p)
    return patienten

def borrar(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patienten WHERE id = ?", (id,))
    conn.commit()