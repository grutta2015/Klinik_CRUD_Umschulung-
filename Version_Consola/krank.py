# -*- coding: utf-8 -*-
import meineklasse
import msvcrt
import re
from datetime import datetime
import os
import datenbank


patienten_list = []
datenbank.inicializar()
patienten_list = datenbank.load()  # reemplaza tu lista vacía


#os.system('color 0A')  # ← agrega esta línea
os.system('color')

VERDE = "\033[92m"
RESET = "\033[0m"

_print_original = print

def print(*args, **kwargs):
    final_de_linea = kwargs.pop('end', '\n')
    sep = kwargs.pop('sep', ' ')
    if args:
        texto = sep.join(str(a) for a in args)
        _print_original(f"{VERDE}{texto}{RESET}", end=final_de_linea, **kwargs)
    else:
        _print_original(end=final_de_linea, **kwargs)

_input_original = input

def input(prompt=""):
    return _input_original(f"{VERDE}{prompt}{RESET}")

###______________________________________________________________________________________


def getch():
    return msvcrt.getwch()

def name_eingabe():
    while True:
        # Recogemos la entrada, quitamos espacios extremos y formateamos
        name = input("Name: ").strip().title()
        
        # Verificamos si es alfabético O es un espacio
        # Esto permite nombres compuestos como "Müller Von Weber"
        if all(c.isalpha() or c.isspace() for c in name) and name != "":
            return name
        else:
            print("Entrada no válida: solo se permiten letras.")
### con all() muy de Python o con replace() son dos formas de hacer lo mismo
def vorname_eingabe():
    while True:
        vorname = input("Vorame: ")
        vorname = vorname.strip().title()  #quita espacio y mete mayusculas
        # Validamos una copia sin espacios, pero retornamos el original
        if vorname.replace(" ", "").isalpha():
            return vorname
        else:
            print("Entrada no válida: solo se permiten letras.")

   

def gebdatum_eingabe():
    while True:
        gebdatum = input("Geburtsdatum (DD.MM.YYYY): ")
        gebdatum = gebdatum.strip().replace(",", ".")
        patron = r"^\d{2}\.\d{2}\.\d{4}$"

        # 1. Primero validas el formato
        if not re.match(patron, gebdatum):
            print("\a✗ Error: Debes usar el formato DD.MM.YYYY")
            continue  # La clave es que continue vuelve al inicio del while y pide la fecha de nuevo.

        try:
            gebdatum = datetime.strptime(gebdatum, "%d.%m.%Y")
        except ValueError:
            print("✗ Error: Fecha inválida (día o mes inexistente)")
            continue

        datum_heute = datetime.now()

        if gebdatum > datum_heute or gebdatum.year < 1900:
           
            print("✗ Error: Ingrese un año válido")
            continue

        return gebdatum.strftime("%d.%m.%Y")

def systemzugang_eingabe():
    systemzugang = datetime.now().strftime("%d.%m.%Y")
    return systemzugang
        

def neues_patient(name, vorname, gebdatum, systemzugang):
    neues_patient_obj = meineklasse.Person(name, vorname, gebdatum, systemzugang)
    patienten_list.append(neues_patient_obj)
    datenbank.guardar(neues_patient_obj)
    

####   ________________PROGRAMM_______________________


try:
    
    while True:

        r = 50
        print('\n┌' + '─' * r + '┐')
        print('│' + '  Klinik 2001 '.center(r) + '│')
        print('└' + '─' * r + '┘')
        print(' ' * 32 + 'Datum: ', systemzugang_eingabe())
        print('┌' + '─' * r + '┐')
        print('│' + '1) Neuer Patient'.ljust(r) + '│')
        print('│' + '2) Patienten Suchen'.ljust(r) + '│')
        print('│' + '3) Patienten Liste'.ljust(r) + '│')
        print('│' + '4) Patienten Löschen'.ljust(r) + '│')
        #print('│' + '5) Liste durch Datei Type'.ljust(r) + '│')
        print('│' + '6) Ende'.ljust(r) + '│')
        print('└' + '─' * r + '┘')
        
        print("--> Bitte wählen: ", end='', flush=True)
        eingabe_option = getch()
        print(eingabe_option)  # para que el número aparezca en pantalla

        match eingabe_option:

            case '1':
                name = name_eingabe()
                vorname = vorname_eingabe()
                gebdatum = gebdatum_eingabe()
                systemzugang = systemzugang_eingabe()

                neues_patient(name, vorname, gebdatum, systemzugang)
                neues = patienten_list[-1] #  -1 como índice significa "el último elemento".
                print(f"\n✓ Neuen Patient Gespeichert")
                print(f"Name: {neues.get_name()}")
                print(f"Vorname: {neues.get_vorname()}")
                print(f"Gebursdatum: {neues.get_gebdatum()}")
                print(f"Systemzugang: {neues.get_systemzugang()}")
                print('Edad: ', neues.get_edad())
                        
            case '2':
                while True:

                    r = 50
                    print('\n┌' + '─' * r + '┐')
                    print('│' + '  Suchen'.center(r) + '│')
                    print('└' + '─' * r + '┘')
                
                    print('┌' + '─' * r + '┐')
                    print('│' + '1) Name der Patient: '.ljust(r) + '│')
                    print('│' + '2) Zurück'.ljust(r) + '│')
                    print('└' + '─' * r + '┘')
                    
                    print("--> Bitte wählen: ", end='', flush=True)
                    eingabe_option = getch()
                    print(eingabe_option)  # para que el número aparezca en pantalla

                    match eingabe_option:
                        case '1':
                            name = name_eingabe()
                            gefunden = False
                            for patient in patienten_list:   # iterieren (?) aufzählen la lista del inventar
                                if patient.get_name() == name:
                                    print(f"\n✓ Patient Gefunden!")
                                    print(f"Name: {patient.get_name()}")
                                    print(f"Vorname: {patient.get_vorname()}")
                                    print(f"Gebursdatum: {patient.get_gebdatum()}")
                                    print(f"Systemzugang: {patient.get_systemzugang()}")
                                    print('Edad: ', patient.get_edad())
                                    gefunden = True
                                    break
                            if not gefunden:
                                print(f"\n✗ Kein Patient mit der Name '{name}' gefunden.")            

                        case '2':
                            break

                        case _:
                            print("\a\nUngültige Eingabe. Bitte versuchen Sie es erneut.")
                
            case '3':
                r = 50
                print('\n┌' + '─' * r + '┐')
                print('│' + '  Patienten Liste'.center(r) + '│')
                print('└' + '─' * r + '┘')

                if patienten_list:                                  # Enumerate
                    for i, patient in enumerate (patienten_list, 1):# sirve para numerar los elementos de una lista mientras los recorres.
                        print(f"\n{i}. Name: {patient.get_name()}")
                        print(f"Vorname: {patient.get_vorname()}")
                        print(f"Gebursdatum: {patient.get_gebdatum()}")
                        print('Edad: ', patient.get_edad())
                        print(f"Systemzugang: {patient.get_systemzugang()}")
                else:
                    print(f"\n✗ La lista esta vacia.")
                        
            
            case '4':
                    r = 50
                    print('\n┌' + '─' * r + '┐')
                    print('│' + '  Patienten Löschen'.center(r) + '│')
                    print('└' + '─' * r + '┘')

                    print("\nNames des zu löschenden Patienten: ")
                    name = name_eingabe()

                    # 1. Buscar todas las coincidencias y guardarlas con su índice original
                    coincidencias = []
                    for i, patient in enumerate(patienten_list):
                        if patient.get_name() == name:
                            coincidencias.append((i, patient))  # guardamos índice real y paciente

                    # 2. Mostrar resultados según cuántas coincidencias hay
                    if not coincidencias:
                        print("✗ Es sind keine Patienten mit diesem Namen in der Liste.")

                    elif len(coincidencias) == 1:
                        # Solo uno: mostrar y confirmar
                        i, patient = coincidencias[0]
                        print(f"\nPatient gefunden:")
                        print(f"  Name:         {patient.get_name()}")
                        print(f"  Vorname:      {patient.get_vorname()}")
                        print(f"  Geburtsdatum: {patient.get_gebdatum()}")
                        print(f"  Edad:         {patient.get_edad()}")
                        print(f"  Systemzugang: {patient.get_systemzugang()}")

                        confirm = input("\n¿Seguro que deseas eliminar este paciente? (s/n): ").strip().lower()
                        if confirm == 's':
                            patienten_list.pop(i)
                            datenbank.borrar(patient.get_id())  # lo borramos de la lista
                            print(f"✓ Patient '{patient.get_vorname()} {patient.get_name()}' wurde erfolgreich gelöscht.")
                        else:
                            print("✗ Vorgang abgebrochen.")

                    else:
                        # Varios: mostrar todos numerados y pedir elección
                        print(f"\n{len(coincidencias)} Patienten mit dem Namen '{name}' gefunden:\n")
                        for num, (i, patient) in enumerate(coincidencias, 1):
                            print(f"  {num}. Vorname:      {patient.get_vorname()}")
                            print(f"     Geburtsdatum: {patient.get_gebdatum()}")
                            print(f"     Edad:         {patient.get_edad()}")
                            print(f"     Systemzugang: {patient.get_systemzugang()}")
                            print()

                        try:
                            eleccion = int(input(f"¿Cuál deseas eliminar? (1-{len(coincidencias)}, 0 para cancelar): "))
                            if eleccion == 0:
                                print("✗ Vorgang abgebrochen.")
                            elif 1 <= eleccion <= len(coincidencias):
                                indice_real, patient = coincidencias[eleccion - 1]
                                patienten_list.pop(indice_real)
                                datenbank.borrar(patient.get_id())  # lo borramos de la lista
                                print(f"✓ Patient '{patient.get_vorname()} {patient.get_name()}' wurde erfolgreich gelöscht.")
                            else:
                                print("✗ Ungültige Auswahl.")
                        except ValueError:
                            print("✗ Bitte eine gültige Zahl eingeben.")
     
            case '6':
                
                print("\nAuf Wiedersehen!")
                break

            case _:
                print("\a\n✗ Ungültige Eingabe. Bitte versuchen Sie es erneut.")
finally:
    datenbank.cerrar()