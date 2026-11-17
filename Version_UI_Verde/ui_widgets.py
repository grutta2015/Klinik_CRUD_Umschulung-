# ui_widgets.py
# Funciones constructoras de widgets — solo crean y devuelven widgets, sin lógica.
# No importa nada de UI — es el nivel más bajo, lo usan ui.py y ui_panel_derecha.py
# EXTRAIDO de ui.py — mismas funciones, sin cambios de comportamiento.

import customtkinter as ctk
import config

# Paleta activa — se carga una vez al importar el módulo
_p = config.get_palette()


def _eingabefeld(parent, texto, row, readonly=None):
    """Crea una fila con label + entry y la devuelve."""
    
    label = ctk.CTkLabel(parent, text=texto, anchor="w", text_color=_p["LABEL_FARBE"])
    label.grid(row=row, column=1, padx=(15, 5), pady=5, sticky="w")
    entry = ctk.CTkEntry(parent, width=config.ENTRY_BREITE)
    entry.grid(row=row, column=2, padx=(15, 15), pady=5)
    
    readonly = readonly if readonly is not None else False
    if readonly:
        entry.configure(state="disabled", fg_color=_p["FRAME_BG"], text_color=_p["ENTRY_TEXT"])
    return entry

  


def _btn(texto, parent, comando, color=_p["BTN_NEU_BG"], hover_color=_p["ENTRY_BORDER"],
         width=150, text_color=_p["BTN_PRIM_TEXT"], negrita=False, 
         anchor="center", row=None, column=None, columnspan=None, pady=None, padx=None, height=36):
    negri = "bold" if negrita else "normal"
    boton = ctk.CTkButton(
        master=parent,
        text=texto,
        command=comando,
        fg_color=color,
        hover_color=hover_color,   # ← nuevo
        width=width,
        text_color=text_color,
        anchor=anchor,
        font=ctk.CTkFont(size=config.SCHRIFT_BTN_GROESSE, weight=negri),
        height=height,
    )
    if row is not None and column is not None:
        boton.grid(row=row, column=column, columnspan=columnspan, pady=pady, padx=padx)
    return boton


def _separador(parent, row=None, column=None, columnspan=None, pady=None, width=None):
    frame = ctk.CTkFrame(parent, height=2, fg_color=_p["TITEL_FARBE"], width=width)
    if row is not None and column is not None:
        frame.grid(row=row, column=column, columnspan=columnspan, pady=pady)
    else:
        frame.pack(fill="x", padx=20, pady=6)
    return frame


def _label(texto, parent, isTitle=False, size=None, wraplength=0, text_color=None):
    """
    Crea un CTkLabel configurado. 
    Si isTitle es True, usa la fuente de título; 
    si es False, usa el estilo de label estándar.
    """
    # Determinamos la configuración según el tipo
    if isTitle:
        tamano = size if size else config.SCHRIFT_TITEL_GROESSE
        peso = config.SCHRIFT_TITEL_GEWICHT
        color = text_color if text_color else _p["TITEL_FARBE"]
    else:
        tamano = size if size else config.SCHRIFT_BTN_GROESSE
        peso = "normal"
        color = text_color if text_color else _p["LABEL_FARBE"]

    label = ctk.CTkLabel(
        parent,
        text=texto,
        text_color=color,
        font=ctk.CTkFont(size=tamano, weight=peso),
        wraplength=wraplength
    )
    
    return label


