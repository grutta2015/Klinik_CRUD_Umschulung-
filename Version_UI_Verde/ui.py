# -*- coding: utf-8 -*-
import config
import customtkinter as ctk
import ui_widgets as wid
import ui_controller as ctrl # Importamos el cerebro de la UI

# ─── Configuración Ventana ────────────────────────────────────
_p = config.get_palette()
root = ctk.CTk()
root.title(config.FENSTER_TITEL)
root.geometry(f"{config.FENSTER_BREITE}x{config.FENSTER_HOEHE}")
root.update_idletasks()
x = (root.winfo_screenwidth()  // 2) - (config.FENSTER_BREITE // 2)
y = (root.winfo_screenheight() // 2) - (config.FENSTER_HOEHE  // 2)
root.geometry(f"{config.FENSTER_BREITE}x{config.FENSTER_HOEHE}+{x}+{y}")
ctk.set_appearance_mode(config.APPEARANCE_MODE)

## ------- Funciones para borrar y dibujar ventanas -------------------
def limpiar_frame(frame):
    """Elimina todos los widgets dentro del frame dado."""
    for widget in frame.winfo_children():
        widget.destroy()
        
def dibujar_frame(frame, tipo):
    """Dibuja el contenido del frame según el tipo especificado."""
    limpiar_frame(frame)
    if tipo == "neu_patient":
        window_neu_patient()
    elif tipo == "suchen_patient":
        window_suchen_patient()
    elif tipo == "anzeigen_patient":
        window_anzeigen_patient()

def window_neu_patient():

    frame_window = ctk.CTkFrame(frame_principal, width=470, 
                                height=350, fg_color=_p["SIDEBAR_BG"],
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_window.pack(side="left", padx=(150, 10), pady=50, fill="both")
    frame_window.pack_propagate(False)
    frame_window.grid_propagate(False)
    
    frame_campos = ctk.CTkFrame(frame_window, width=480, 
                                height=380, fg_color="transparent")
    frame_campos.pack(side="left", padx=(20, 15), pady=20, fill="both")

    wid._label("Neuer Patient", frame_campos, isTitle=True).grid(row=0, 
                                 column=2, columnspan=2, padx=5, pady=(30, 5))

    entry_name       = wid._eingabefeld(frame_campos, "Name",         1)
    entry_vorname    = wid._eingabefeld(frame_campos, "Vorname",      2)
    entry_geburt     = wid._eingabefeld(frame_campos, "Geburtsdatum", 3)
    entry_telefon    = wid._eingabefeld(frame_campos, "Telefon",      4)
    entry_email      = wid._eingabefeld(frame_campos, "E-Mail",       5)
    entry_strasse    = wid._eingabefeld(frame_campos, "Straße",       6)
    entry_hausnummer = wid._eingabefeld(frame_campos, "Hausnummer",   7)
    entry_plz        = wid._eingabefeld(frame_campos, "PLZ",          8)
    entry_ort        = wid._eingabefeld(frame_campos, "Ort",          9)

    label_id = wid._label("ID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_id.grid(row=2, column=4, padx=15, sticky="w")

    label_adresse_id = wid._label("AID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_adresse_id.grid(row=6, column=4, padx=15, sticky="w")

    label_error = wid._label("", frame_campos, text_color=_p["FEHLER_FARBE"], wraplength=300)
    label_error.grid(row=13, column=2, padx=15, pady=10)

    # ─── INYECCIÓN DE WIDGETS AL CONTROLADOR ──────────────────────
    ctrl.gui["name"]         = entry_name
    ctrl.gui["vorname"]      = entry_vorname
    ctrl.gui["geburt"]       = entry_geburt
    ctrl.gui["telefon"]      = entry_telefon
    ctrl.gui["email"]        = entry_email
    ctrl.gui["strasse"]      = entry_strasse
    ctrl.gui["hausnummer"]   = entry_hausnummer
    ctrl.gui["plz"]          = entry_plz
    ctrl.gui["ort"]          = entry_ort
    ctrl.gui["id_label"]     = label_id
    ctrl.gui["id_adresse"]   = label_adresse_id
    ctrl.gui["error_label"]  = label_error

    ctrl.limpiar_campos()
    ctrl.gui["error_label"].configure(text="")

   # ─── Botones Speichern y Abrechen ─────────────────────────────
    frame_Boton = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_Boton.grid(row=12, column=2, columnspan=2, pady=8)

    wid._btn("💾 Speichern", frame_Boton, 
           ctrl.speichern, color=_p["BTN_NEU_BG"], 
           text_color=_p["BTN_PRIM_TEXT"], 
           anchor="w", width=100).pack(side="left", padx=7, pady=7)
    
    wid._btn("✗ Abrechen", frame_Boton,
           lambda: dibujar_frame(frame_principal, "suchen_patient"),
           color=_p["BTN_NEU_BG"], 
           text_color=_p["BTN_PRIM_TEXT"], 
           anchor="w", width=100).pack(side="right", padx=7, pady=7)

def window_suchen_patient():
    frame_busqueda = ctk.CTkFrame(frame_principal, fg_color=_p["SIDEBAR_BG"],
                                 corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_busqueda.pack(pady=20, padx=50, fill="both", expand=True)

    wid._label("Patienten Suchen", frame_busqueda, isTitle=True).pack(pady=(30, 5), padx=10)

    entry_suchen = ctk.CTkEntry(frame_busqueda, width=400, 
                                placeholder_text="🔍 Name oder Vorname eingeben...")
    entry_suchen.pack(pady=(5,10))

    frame_res = ctk.CTkScrollableFrame(frame_busqueda, fg_color="transparent")
    frame_res.pack(fill="both", expand=True, padx=20, pady=10)

    def _filtrar_lista(event):
        for widget in frame_res.winfo_children():
            widget.destroy()

        texto = entry_suchen.get().lower()
        if not texto: return

        for p, a in ctrl.filtrar_list_busqueda_dinamica(texto):
            fila = ctk.CTkFrame(frame_res, fg_color=_p["FRAME_BG"])
            fila.pack(fill="x", pady=2, padx=5)
            adresse = f"{a.get_strasse()} {a.get_hausnummer()} {a.get_plz()} {a.get_ort()}" if a else "—"
            ctk.CTkLabel(fila, text=f"{p.get_name()} {p.get_vorname()} ({p.get_gebdatum()}) | {adresse}").pack(side="left", padx=10)
            wid._btn("👁", fila, lambda p=p: [dibujar_frame(frame_principal, "anzeigen_patient"),
                                            ctrl.mostrar_patient(ctrl.alle_patienten.index(p))],
                    width=25, height=25, color=_p["BTN_NEU_BG"]).pack(side="right", padx=3, pady=3)

    entry_suchen.bind("<KeyRelease>", _filtrar_lista)

def window_anzeigen_patient():

    frame_window = ctk.CTkFrame(frame_principal, width=470, 
                                height=350, fg_color=_p["SIDEBAR_BG"],
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_window.pack(side="left", padx=(150, 10), pady=50, fill="both")
    frame_window.pack_propagate(False)
    frame_window.grid_propagate(False)
    
    frame_campos = ctk.CTkFrame(frame_window, width=480, 
                                height=380, fg_color="transparent")
    frame_campos.pack(side="left", padx=(20, 15), pady=20, fill="both")

    wid._label("Patient Information", frame_campos, isTitle=True).grid(row=0, 
                                 column=2, columnspan=2, padx=5, pady=(30,5))

    entry_name       = wid._eingabefeld(frame_campos, "Name",         1)
    entry_vorname    = wid._eingabefeld(frame_campos, "Vorname",      2)
    entry_geburt     = wid._eingabefeld(frame_campos, "Geburtsdatum", 3)
    entry_telefon    = wid._eingabefeld(frame_campos, "Telefon",      4)
    entry_email      = wid._eingabefeld(frame_campos, "E-Mail",       5)
    entry_strasse    = wid._eingabefeld(frame_campos, "Straße",       6)
    entry_hausnummer = wid._eingabefeld(frame_campos, "Hausnummer",   7)
    entry_plz        = wid._eingabefeld(frame_campos, "PLZ",          8)
    entry_ort        = wid._eingabefeld(frame_campos, "Ort",          9)

    label_id = wid._label("ID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_id.grid(row=2, column=4, padx=15, sticky="w")

    label_adresse_id = wid._label("AID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_adresse_id.grid(row=6, column=4, padx=15, sticky="w")

    label_error = wid._label("", frame_campos, text_color=_p["FEHLER_FARBE"], wraplength=300)
    label_error.grid(row=14, column=2, padx=15, pady=10)

    # ─── INYECCIÓN DE WIDGETS AL CONTROLADOR ──────────────────────
    ctrl.gui["name"]         = entry_name
    ctrl.gui["vorname"]      = entry_vorname
    ctrl.gui["geburt"]       = entry_geburt
    ctrl.gui["telefon"]      = entry_telefon
    ctrl.gui["email"]        = entry_email
    ctrl.gui["strasse"]      = entry_strasse
    ctrl.gui["hausnummer"]   = entry_hausnummer
    ctrl.gui["plz"]          = entry_plz
    ctrl.gui["ort"]          = entry_ort
    ctrl.gui["id_label"]     = label_id
    ctrl.gui["id_adresse"]   = label_adresse_id
    ctrl.gui["error_label"]  = label_error

    ctrl.gui["error_label"].configure(text="")

   # ─── Botones: Recetar Med, Ver Recetado, Abrechen ─────────────
   # fila arriba: Recetar Med | Ver Recetado
   # fila abajo:  Abrechen centrado
    frame_Boton_arriba = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_Boton_arriba.grid(row=12, column=2, columnspan=2, pady=(8, 2))

    wid._btn("Recetar Med", frame_Boton_arriba,
           window_vademecum, color=_p["BTN_NEU_BG"],
           text_color=_p["BTN_PRIM_TEXT"],
           anchor="center", width=100).pack(side="left", padx=7)

    wid._btn("Ver Recetado", frame_Boton_arriba,
           window_recetado, color=_p["BTN_NEU_BG"],
           text_color=_p["BTN_PRIM_TEXT"],
           anchor="center", width=100).pack(side="left", padx=7)

    frame_Boton_abajo = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_Boton_abajo.grid(row=13, column=2, columnspan=2, pady=(7, 8))

    wid._btn("✗ Abrechen", frame_Boton_abajo,
           lambda: dibujar_frame(frame_principal, "suchen_patient"),
           color=_p["BTN_NEU_BG"],
           text_color=_p["BTN_PRIM_TEXT"],
           anchor="center", width=100).pack(padx=7)

def window_vademecum():
    vademecum_popup = ctk.CTkToplevel()
    vademecum_popup.grab_set()
    vademecum_popup.title("Vademecum")
    vademecum_popup.geometry("650x600")
    vademecum_popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - 325
    y = root.winfo_y() + (root.winfo_height() // 2) - 300
    vademecum_popup.geometry(f"650x600+{x}+{y}")
    vademecum_popup.attributes("-topmost", True)

    frame_vademecum = ctk.CTkFrame(vademecum_popup, width=600, 
                                height=590, fg_color=_p["SIDEBAR_BG"],
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_vademecum.pack(padx=10, pady=10, fill="both")
    frame_vademecum.pack_propagate(False)

    wid._label("VADEMECUM", frame_vademecum, isTitle=True).pack(pady=(30, 5), padx=10)

    entry_suchen = ctk.CTkEntry(frame_vademecum, width=400, 
                                placeholder_text="🔍 Medikamente Name eingeben...")
    entry_suchen.pack(pady=(5,10))

    frame_res = ctk.CTkScrollableFrame(frame_vademecum, fg_color="transparent")
    frame_res.pack(fill="both", expand=True, padx=20, pady=10)

    def _filtrar_lista_vademecum(event):
        for widget in frame_res.winfo_children():
            widget.destroy()

        texto = entry_suchen.get().lower()
        if not texto: return

        for m in ctrl.filtrar_list_busqueda_vademecum(texto):
            fila = ctk.CTkFrame(frame_res, fg_color=_p["FRAME_BG"])
            fila.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(fila, text=f"{m.get_name()} {m.get_wirkstoff()} | ({m.get_dosis()}) ").pack(side="left", padx=10)
            wid._btn("👁", fila, lambda m=m: window_anzeigen_medicament(m),
                    width=25, height=25, color=_p["BTN_NEU_BG"]).pack(side="right", padx=3, pady=3)

    entry_suchen.bind("<KeyRelease>", _filtrar_lista_vademecum)

    def window_anzeigen_medicament(m):
        # popup para ver el medicamento seleccionado del vademecum,
        # ingresar frequenz y datum, y recetarlo al paciente actual
        medicament_popup = ctk.CTkToplevel()
        medicament_popup.grab_set()
        medicament_popup.title("Medikament Information")
        medicament_popup.geometry("550x250")
        x = root.winfo_x() + (root.winfo_width() // 2) - 275
        y = root.winfo_y() + (root.winfo_height() // 2) - 125
        medicament_popup.geometry(f"550x250+{x}+{y}")
        medicament_popup.attributes("-topmost", True)

        frame_medicament = ctk.CTkFrame(medicament_popup, width=450,
                                        height=240, fg_color=_p["SIDEBAR_BG"],
                                        corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
        frame_medicament.pack(padx=10, pady=10, fill="both")
        frame_medicament.pack_propagate(False)

        # título: nombre y wirkstoff del medicamento seleccionado
        wid._label(f"{m.get_name()} | {m.get_wirkstoff()}", frame_medicament, isTitle=True, size=12).pack(
             pady=(15, 10), padx=(155, 10), anchor="w")
        
        frame_hardcoded = ctk.CTkFrame(frame_medicament, fg_color="transparent")
        frame_hardcoded.pack(padx=(70, 20), pady=10, fill="both")

        entry_frequenz = wid._eingabefeld(frame_hardcoded, "Frequenz", 0)  # ej: "2x täglich"
        entry_datum    = wid._eingabefeld(frame_hardcoded, "Datum",    1)  # ej: "26.04.2026"

        # label para errores de validación dentro del popup
        label_error_popup = wid._label("", frame_hardcoded, text_color=_p["FEHLER_FARBE"], wraplength=250)
        label_error_popup.grid(row=2, column=2, padx=15, pady=(5, 0))

        def _guardar():
            # lee frequenz y datum, valida, guarda la prescripción vinculada al paciente actual
            ok, msg = ctrl.verschreibung_speichern(m, entry_frequenz.get(), entry_datum.get())
            color = _p["BESTAETIGUNG_FARBE"] if ok else _p["FEHLER_FARBE"]
            label_error_popup.configure(text=msg, text_color=color)
            if ok:
                medicament_popup.after(800, medicament_popup.destroy)  # cierra tras confirmación

        wid._btn("💾 Speichern", frame_hardcoded,
               _guardar, color=_p["BTN_NEU_BG"],
               text_color=_p["BTN_PRIM_TEXT"],
               anchor="center", width=100,
               row=3, column=2, pady=(10, 0))

def window_recetado():
    recetado_popup = ctk.CTkToplevel()
    recetado_popup.grab_set()
    recetado_popup.title("Medicamentos Recetados")
    recetado_popup.geometry("650x650")  # ampliado para que entre el label de error
    recetado_popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - 325
    y = root.winfo_y() + (root.winfo_height() // 2) - 325
    recetado_popup.geometry(f"650x650+{x}+{y}")
    recetado_popup.attributes("-topmost", True)

    frame_recetado = ctk.CTkFrame(recetado_popup, width=600, 
                                height=640, fg_color=_p["SIDEBAR_BG"],
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_recetado.pack(padx=10, pady=10, fill="both")
    frame_recetado.pack_propagate(False)

    wid._label("Medicamentos Recetados", frame_recetado, 
               isTitle=True).pack(pady=(30, 5), padx=10)

    # label de error — se muestra si vademecum_get_by_id devuelve None
    # mismo patrón que label_error_popup en window_anzeigen_medicament
    label_error_recetado = wid._label("", frame_recetado, text_color=_p["FEHLER_FARBE"], wraplength=400)
    label_error_recetado.pack(pady=(0, 5))

    frame_res = ctk.CTkScrollableFrame(frame_recetado, fg_color="transparent")
    frame_res.pack(fill="both", expand=True, padx=20, pady=10)

    verschreibungen = ctrl.patient_verschreibungen_load()
    verschreibungen_reversed = list(reversed(verschreibungen))

    if not verschreibungen_reversed:
        wid._label("Keine Medikamente verschrieben.", frame_res).pack(pady=10)
    else:
        for v in verschreibungen_reversed:
            m = ctrl.vademecum_get_by_id(v.get_medikamentID())

            # guarda de seguridad — si el MID no existe en el vademecum mostramos error
            # en condiciones normales no debería ocurrir
            if m is None:
                label_error_recetado.configure(
                    text=f"Error: Medikament {v.get_medikamentID()} nicht im Vademecum gefunden.")
                continue  # salta esta fila y sigue con las demás

            fila = ctk.CTkFrame(frame_res, fg_color=_p["FRAME_BG"])
            fila.pack(fill="x", pady=2, padx=5)

            ctk.CTkLabel(fila, text=f"{m.get_name()} | {m.get_wirkstoff()} | {v.get_frequenz()} | {v.get_datum()}").pack(side="left", padx=10)

            wid._btn("🗑", fila,
                    lambda v=v: [ctrl.verschreibung_delete_von_patient(v), recetado_popup.destroy(), window_recetado()],
                    width=25, height=25, color=_p["BTN_DEL_BG"],
                    text_color=_p["BTN_DEL_TEXT"]).pack(side="right", padx=3, pady=3)

def window_bearbeiten():
    # abre una ventana igual a window_neu_patient pero con los datos del paciente actual cargados
    # permite editar nombre, dirección, etc. — NO los medicamentos recetados
    # al guardar llama a ctrl.bearbeiten que actualiza el objeto y lo persiste en datenbank

    # si no hay paciente seleccionado no hacemos nada
    if not ctrl.alle_patienten:
        return

    limpiar_frame(frame_principal)

    frame_window = ctk.CTkFrame(frame_principal, width=470,
                                height=350, fg_color=_p["SIDEBAR_BG"],
                                corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
    frame_window.pack(side="left", padx=(150, 10), pady=50, fill="both")
    frame_window.pack_propagate(False)
    frame_window.grid_propagate(False)

    frame_campos = ctk.CTkFrame(frame_window, width=480,
                                height=380, fg_color="transparent")
    frame_campos.pack(side="left", padx=(20, 15), pady=20, fill="both")

    wid._label("Patient bearbeiten", frame_campos, isTitle=True).grid(row=0,
                                 column=2, columnspan=2, padx=5, pady=(30, 5))

    # mismos campos que window_neu_patient — mismo orden, mismo estilo
    entry_name       = wid._eingabefeld(frame_campos, "Name",         1)
    entry_vorname    = wid._eingabefeld(frame_campos, "Vorname",      2)
    entry_geburt     = wid._eingabefeld(frame_campos, "Geburtsdatum", 3)
    entry_telefon    = wid._eingabefeld(frame_campos, "Telefon",      4)
    entry_email      = wid._eingabefeld(frame_campos, "E-Mail",       5)
    entry_strasse    = wid._eingabefeld(frame_campos, "Straße",       6)
    entry_hausnummer = wid._eingabefeld(frame_campos, "Hausnummer",   7)
    entry_plz        = wid._eingabefeld(frame_campos, "PLZ",          8)
    entry_ort        = wid._eingabefeld(frame_campos, "Ort",          9)

    label_id = wid._label("ID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_id.grid(row=2, column=4, padx=15, sticky="w")

    label_adresse_id = wid._label("AID: —", frame_campos, text_color=_p["ID_FARBE"])
    label_adresse_id.grid(row=6, column=4, padx=15, sticky="w")

    label_error = wid._label("", frame_campos, text_color=_p["FEHLER_FARBE"], wraplength=300)
    label_error.grid(row=13, column=2, padx=15, pady=10)

    # ─── INYECCIÓN DE WIDGETS AL CONTROLADOR ──────────────────────
    # mismo patrón que window_neu_patient y window_anzeigen_patient
    ctrl.gui["name"]        = entry_name
    ctrl.gui["vorname"]     = entry_vorname
    ctrl.gui["geburt"]      = entry_geburt
    ctrl.gui["telefon"]     = entry_telefon
    ctrl.gui["email"]       = entry_email
    ctrl.gui["strasse"]     = entry_strasse
    ctrl.gui["hausnummer"]  = entry_hausnummer
    ctrl.gui["plz"]         = entry_plz
    ctrl.gui["ort"]         = entry_ort
    ctrl.gui["id_label"]    = label_id
    ctrl.gui["id_adresse"]  = label_adresse_id
    ctrl.gui["error_label"] = label_error

    # carga los datos del paciente actual en los campos — mismo que mostrar_patient
    # pero sin bloquear los campos, para que el usuario pueda editarlos
    ctrl.mostrar_patient(ctrl.current_index[0])
    for clave in ["name", "vorname", "geburt", "telefon", "email", "strasse", "hausnummer", "plz", "ort"]:
        ctrl.gui[clave].configure(state="normal")

    # ─── Botones Aktualisieren y Abrechen ─────────────────────────
    frame_Boton = ctk.CTkFrame(frame_campos, fg_color="transparent")
    frame_Boton.grid(row=12, column=2, columnspan=2, pady=8)

    wid._btn("💾 Aktualisieren", frame_Boton,
           lambda: [ctrl.bearbeiten(), dibujar_frame(frame_principal, "anzeigen_patient")],
           color=_p["BTN_NEU_BG"],
           text_color=_p["BTN_PRIM_TEXT"],
           anchor="w", width=120).pack(side="left", padx=7, pady=7)

    wid._btn("✗ Abrechen", frame_Boton,
           lambda: dibujar_frame(frame_principal, "anzeigen_patient"),
           color=_p["BTN_NEU_BG"],
           text_color=_p["BTN_PRIM_TEXT"],
           anchor="w", width=100).pack(side="right", padx=7, pady=7)


###______________________________ UI ______________________________

#----------------------- Sidebar a la izquierda -------------------
sidebar_links = ctk.CTkFrame(root, width=config.SIDEBAR_BREITE, 
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"], 
                             fg_color=_p["SIDEBAR_BG"])
sidebar_links.pack(side="left", fill="y", padx=(10, 5), pady=10)
sidebar_links.pack_propagate(False)
sidebar_links.grid_propagate(False)
sidebar_links.columnconfigure(0, weight=1, minsize=config.SIDEBAR_BREITE)
sidebar_links.columnconfigure(1, weight=0, minsize=0)

# ----------------------: Frame Principal -----------------------------
frame_principal = ctk.CTkFrame(root, fg_color=_p["FRAME_BG"],
                             corner_radius=config.PALETTEN[config.AKTIVE_PALETTE]["FRAME_CORNER_RADIUS"])
frame_principal.pack(side="left", padx=(5, 10), pady=10, fill="both", expand=True)

wid._label("Klinik 2001", sidebar_links, 
        isTitle=True).grid(row=0, 
                           column=0, 
                           columnspan=2, 
                           pady=(20, 1), sticky="ew")

wid._label("Version 2.0", sidebar_links, 
        isTitle=False, size=11).grid(row=1,
                                     column=0,
                                     columnspan=2,
                                     pady=(1, 1), sticky="ew")

#--- Botones Arriba: Neu, Suchen, Anzeigen
sidebar_links.rowconfigure(2, weight=0)

wid._separador(sidebar_links, 
           width=config.SIDEBAR_BREITE - 40).grid(row=2, 
                                                  column=0, 
                                                  columnspan=2, 
                                                  pady=(90, 5))

#- Botón Neu
wid._btn("➕ Neu", sidebar_links, 
           lambda: dibujar_frame(frame_principal, "neu_patient"), 
           text_color=_p["BTN_NEU_TEXT"], 
           anchor="w", row=3, column=0, 
           columnspan=2, pady=(15, 5))

#- Botón Suchen
wid._btn("🔍 Suchen", sidebar_links, 
           lambda: dibujar_frame(frame_principal, "suchen_patient"), 
           color="transparent", text_color=_p["BTN_NEU_TEXT"], 
           anchor="w", row=4, column=0, columnspan=2, pady=5)

# #- Botón Anzeigen
# wid._btn("👁 Anzeigen", sidebar_links, 
#            lambda: dibujar_frame(frame_principal, "anzeigen"), 
#            color="transparent", text_color=_p["BTN_NEU_TEXT"], 
#            anchor="w", row=5, column=0, columnspan=2, pady=5)

#--- Botones Abajo: Bearbeiten, Löschen
sidebar_links.rowconfigure(10, weight=1) # empuja los botones hacia abajo

#- Botón Bearbeiten
wid._btn("⚙ Bearbeiten", sidebar_links, 
           window_bearbeiten, color=_p["BTN_PRIM_BG"], 
           text_color=_p["BTN_PRIM_TEXT"],
           row=11, column=0, columnspan=2, pady=5)

#- Botón Löschen
wid._btn("🗑 Löschen", sidebar_links, 
           ctrl.delete, color=_p["BTN_DEL_BG"], 
           text_color=_p["BTN_DEL_TEXT"], 
           negrita=True, row=12, column=0, 
           columnspan=2, pady=(5, 15))
