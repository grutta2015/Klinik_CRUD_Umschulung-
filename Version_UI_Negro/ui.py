"""
ui.py
Interfaz gráfica con CustomTkinter.
"""

import customtkinter as ctk
from tkinter import messagebox
import config
import logic

C = config.C


# ── Helpers ───────────────────────────────────────────────────

def _entry(parent, placeholder="", width=280):
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        fg_color=C["bg_card"],
        border_color=C["borde"],
        text_color=C["texto"],
        placeholder_text_color=C["texto_suave"],
        font=config.FONT_NORMAL,
        corner_radius=config.CORNER_R,
    )


def _label(parent, text, bold=False, small=False):
    font = config.FONT_BOLD if bold else (config.FONT_SMALL if small else config.FONT_NORMAL)
    return ctk.CTkLabel(parent, text=text, text_color=C["texto"], font=font)


def _btn(parent, text, command, danger=False, width=140, disabled=False):
    if disabled:
        color  = C["bg_card"]
        tcolor = C["texto_suave"]
        state  = "disabled"
    else:
        color  = C["danger"] if danger else C["acento"]
        tcolor = C["bg_main"]
        state  = "normal"
    return ctk.CTkButton(
        parent, text=text, command=command,
        fg_color=color,
        hover_color=C["hover"],
        text_color=tcolor,
        font=config.FONT_BOLD,
        corner_radius=config.CORNER_R,
        width=width,
        state=state,
    )


def _separador(parent):
    ctk.CTkFrame(parent, height=1, fg_color=C["borde"]).pack(fill="x", padx=20, pady=6)


# ── Ventana de solo lectura (doble click) ────────────────────

class VerVentana(ctk.CTkToplevel):

    CAMPOS = [
        ("Name",          "get_name"),
        ("Vorname",       "get_vorname"),
        ("Geburtsdatum",  "get_gebdatum"),
        ("Alter",         "get_edad"),
        ("Telefon",       "get_telefono"),
        ("E-Mail",        "get_email"),
        ("Adresse",       "get_direccion"),
        ("Systemzugang",  "get_systemzugang"),
    ]

    def __init__(self, parent_app, patient):
        super().__init__()
        self.title(f"{patient.get_vorname()} {patient.get_name()}")
        self.geometry("480x380")
        self.configure(fg_color=C["bg_panel"])
        self.resizable(False, False)
        self.grab_set()
        self._build(patient)

    def _build(self, p):
        _label(self, f"{p.get_vorname()} {p.get_name()}", bold=True).pack(pady=(20, 4))
        _separador(self)

        for i, (etiqueta, getter) in enumerate(self.CAMPOS):
            bg    = C["bg_card"] if i % 2 == 0 else C["bg_panel"]
            valor = str(getattr(p, getter)())
            fila  = ctk.CTkFrame(self, fg_color=bg, corner_radius=0, height=38)
            fila.pack(fill="x")
            fila.pack_propagate(False)

            ctk.CTkLabel(fila, text=etiqueta, width=140, anchor="w",
                         font=config.FONT_BOLD, text_color=C["texto_suave"],
                         ).pack(side="left", padx=(20, 8))
            ctk.CTkLabel(fila, text=valor or "—", anchor="w",
                         font=config.FONT_NORMAL, text_color=C["texto"],
                         ).pack(side="left")

        _btn(self, "Schließen", self.destroy, width=110).pack(pady=16)


# ── Ventana de edición (Toplevel) ─────────────────────────────

class EditarVentana(ctk.CTkToplevel):

    def __init__(self, parent_app, patient, on_close=None):
        super().__init__()
        self.app      = parent_app
        self.patient  = patient
        self.on_close = on_close  # callback al cerrar

        self.title("Patient bearbeiten")
        self.geometry("520x480")
        self.configure(fg_color=C["bg_panel"])
        self.resizable(False, False)
        self.grab_set()

        self._build()

    def _build(self):
        _label(self, "Patient bearbeiten", bold=True).pack(pady=(20, 4))
        _separador(self)

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(padx=30, pady=8, fill="both", expand=True)

        campos = [
            ("Name *",         "name",      self.patient.get_name()),
            ("Vorname *",      "vorname",   self.patient.get_vorname()),
            ("Geburtsdatum *", "gebdatum",  self.patient.get_gebdatum()),
            ("Telefon",        "telefono",  self.patient.get_telefono()),
            ("E-Mail",         "email",     self.patient.get_email()),
            ("Adresse",        "direccion", self.patient.get_direccion()),
        ]

        self.entries = {}
        for i, (lbl, key, valor) in enumerate(campos):
            _label(form, lbl, small=True).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 12))
            e = _entry(form, width=300)
            e.insert(0, valor)
            e.grid(row=i, column=1, sticky="w", pady=5)
            self.entries[key] = e

        self.error_lbl = ctk.CTkLabel(self, text="", text_color=C["danger"], font=config.FONT_SMALL)
        self.error_lbl.pack(pady=(2, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(6, 18))
        _btn(btn_row, "Speichern", self._guardar, width=130).pack(side="left", padx=8)
        _btn(btn_row, "Abbrechen", self._cerrar,  width=110).pack(side="left", padx=8)

    def _guardar(self):
        vals = {k: e.get() for k, e in self.entries.items()}
        ok, msg = logic.validar_todos(vals)
        if not ok:
            self.error_lbl.configure(text=f"✗  {msg}")
            return
        logic.actualizar_patient(self.patient, vals)
        self._cerrar()

    def _cerrar(self):
        if self.on_close:
            self.on_close()
        self.destroy()


# ── Ventana principal ─────────────────────────────────────────

class App(ctk.CTk):

    def __init__(self, patienten_list):
        super().__init__()
        self.patienten_list  = patienten_list
        self.selected_patient = None   # paciente actualmente seleccionado

        self.title(f"{config.APP_NOMBRE}  v{config.APP_VERSION}")
        self.geometry(f"{config.VENTANA_W}x{config.VENTANA_H}")
        self.configure(fg_color=C["bg_main"])
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self._build_layout()
        self._show_frame("lista")

    # ── Layout ───────────────────────────────────────────────

    def _build_layout(self):
        # ── Sidebar ──
        self.sidebar = ctk.CTkFrame(self, width=config.SIDEBAR_W,
                                    fg_color=C["bg_panel"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Título
        ctk.CTkLabel(self.sidebar, text=config.APP_NOMBRE,
                     font=config.FONT_TITLE, text_color=C["acento"]).pack(pady=(28, 4))
        ctk.CTkLabel(self.sidebar, text=f"v{config.APP_VERSION}",
                     font=config.FONT_SMALL, text_color=C["texto_suave"]).pack(pady=(0, 24))
        _separador(self.sidebar)

        # Navegación principal
        nav = [
            ("➕  Neuer Patient",  "nuevo"),
            ("🔍  Suchen",         "buscar"),
            ("📋  Patientenliste", "lista"),
        ]
        self._nav_btns = {}
        for label, key in nav:
            btn = ctk.CTkButton(
                self.sidebar, text=label,
                command=lambda k=key: self._show_frame(k),
                fg_color="transparent", hover_color=C["hover"],
                text_color=C["texto"], font=config.FONT_NORMAL,
                anchor="w", corner_radius=config.CORNER_R,
                width=config.SIDEBAR_W - 20,
            )
            btn.pack(pady=3, padx=10)
            self._nav_btns[key] = btn

        # ── Botones de acción (abajo del sidebar) ──
        # Empujan hacia abajo con un frame expandible de relleno
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        _separador(self.sidebar)

        self.btn_editar = ctk.CTkButton(
            self.sidebar, text="⚙  Bearbeiten",
            command=self._accion_editar,
            fg_color=C["bg_card"],
            hover_color=C["hover"],
            text_color=C["texto_suave"],
            font=config.FONT_NORMAL,
            anchor="w",
            corner_radius=config.CORNER_R,
            width=config.SIDEBAR_W - 20,
            state="disabled",
        )
        self.btn_editar.pack(pady=3, padx=10)

        self.btn_borrar = ctk.CTkButton(
            self.sidebar, text="🗑  Löschen",
            command=self._accion_borrar,
            fg_color=C["bg_card"],
            hover_color=C["hover"],
            text_color=C["texto_suave"],
            font=config.FONT_NORMAL,
            anchor="w",
            corner_radius=config.CORNER_R,
            width=config.SIDEBAR_W - 20,
            state="disabled",
        )
        self.btn_borrar.pack(pady=(0, 20), padx=10)

        # ── Área de contenido ──
        self.content = ctk.CTkFrame(self, fg_color=C["bg_main"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.frames = {
            "nuevo":  NuevoPatientFrame(self.content, self),
            "buscar": BuscarFrame(self.content, self),
            "lista":  ListaFrame(self.content, self),
        }
        for f in self.frames.values():
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _show_frame(self, key):
        self.frames[key].tkraise()
        if key == "lista":
            self.frames["lista"].refresh()
        if key == "buscar":
            self.frames["buscar"].reset()
        for k, btn in self._nav_btns.items():
            btn.configure(
                fg_color=C["bg_card"] if k == key else "transparent",
                text_color=C["acento"] if k == key else C["texto"],
            )

    # ── Selección de paciente ────────────────────────────────

    def seleccionar(self, patient):
        """Activa el paciente seleccionado y habilita los botones de acción."""
        self.selected_patient = patient
        self.btn_editar.configure(
            state="normal",
            fg_color=C["acento"],
            text_color=C["bg_main"],
        )
        self.btn_borrar.configure(
            state="normal",
            fg_color=C["danger"],
            text_color=C["bg_main"],
        )

    def deseleccionar(self):
        """Limpia la selección y desactiva los botones de acción."""
        self.selected_patient = None
        self.btn_editar.configure(
            state="disabled",
            fg_color=C["bg_card"],
            text_color=C["texto_suave"],
        )
        self.btn_borrar.configure(
            state="disabled",
            fg_color=C["bg_card"],
            text_color=C["texto_suave"],
        )

    def _accion_editar(self):
        if not self.selected_patient:
            return
        def on_close():
            self.frames["lista"].refresh()
            self.frames["buscar"]._buscar()
            self.deseleccionar()
        EditarVentana(self, self.selected_patient, on_close=on_close)

    def _accion_borrar(self):
        if not self.selected_patient:
            return
        p = self.selected_patient
        if messagebox.askyesno("Löschen",
                f"Patient '{p.get_vorname()} {p.get_name()}' löschen?"):
            logic.borrar_patient(p, self.patienten_list)
            self.deseleccionar()
            self.frames["lista"].refresh()
            self.frames["buscar"]._buscar()


# ── Vista: Nuevo paciente ─────────────────────────────────────

class NuevoPatientFrame(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=C["bg_main"])
        self.app = app
        self._build()

    def _build(self):
        inner = ctk.CTkFrame(self, fg_color=C["bg_panel"], corner_radius=12)
        inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.72, relheight=0.90)

        _label(inner, "Neuer Patient", bold=True).pack(pady=(24, 2))
        _separador(inner)

        form = ctk.CTkFrame(inner, fg_color="transparent")
        form.pack(padx=30, pady=10, fill="both", expand=True)

        campos = [
            ("Name *",         "name",      ""),
            ("Vorname *",      "vorname",   ""),
            ("Geburtsdatum *", "gebdatum",  ""),          # "DD.MM.YYYY"
            ("Telefon",        "telefono",  ""),           # "z.B. +49 30 123456"
            ("E-Mail",         "email",     ""),           # "z.B. beispiel@mail.com"
            ("Adresse",        "direccion", ""),           # "z.B. Boddinstr. 10"
        ]
        self.entries = {}
        for i, (lbl, key, ph) in enumerate(campos):
            _label(form, lbl, small=True).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 12))
            e = _entry(form, placeholder=ph, width=320)
            e.grid(row=i, column=1, sticky="w", pady=5)
            self.entries[key] = e

        self.error_lbl = ctk.CTkLabel(inner, text="", text_color=C["danger"], font=config.FONT_SMALL)
        self.error_lbl.pack(pady=(2, 0))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(pady=(8, 20))
        _btn(btn_row, "Speichern", self._guardar).pack(side="left", padx=8)
        _btn(btn_row, "Leeren",    self._limpiar, width=100).pack(side="left", padx=8)

    def _limpiar(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.error_lbl.configure(text="", text_color=C["danger"])

    def _guardar(self):
        vals = {k: e.get() for k, e in self.entries.items()}
        ok, msg = logic.validar_todos(vals)
        if not ok:
            self.error_lbl.configure(text_color=C["danger"], text=f"✗  {msg}")
            return
        p = logic.crear_patient(**vals)
        self.app.patienten_list.append(p)
        self._limpiar()
        self.error_lbl.configure(text_color=C["acento"], text="✓  Patient gespeichert.")
        self.after(2500, lambda: self.error_lbl.configure(text=""))


# ── Vista: Buscar ─────────────────────────────────────────────

class BuscarFrame(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=C["bg_main"])
        self.app = app
        self._selected_card = None   # frame de la tarjeta actualmente seleccionada
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=C["bg_panel"], corner_radius=12, height=80)
        top.pack(fill="x", padx=24, pady=(24, 0))
        top.pack_propagate(False)

        row = ctk.CTkFrame(top, fg_color="transparent")
        row.pack(expand=True)
        _label(row, "Name:").pack(side="left", padx=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._buscar())

        self.search_entry = _entry(row, width=300)
        self.search_entry.configure(textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=(0, 8))

        self.result_frame = ctk.CTkScrollableFrame(
            self, fg_color=C["bg_panel"], corner_radius=12)
        self.result_frame.pack(fill="both", expand=True, padx=24, pady=12)

    def reset(self):
        self.search_var.set("")
        self._selected_card = None
        self.app.deseleccionar()
        for w in self.result_frame.winfo_children():
            w.destroy()

    def _buscar(self):
        self._selected_card = None
        self.app.deseleccionar()
        for w in self.result_frame.winfo_children():
            w.destroy()

        texto = self.search_var.get().strip()
        if not texto:
            return

        texto_lower = texto.lower()
        resultados = [
            p for p in self.app.patienten_list
            if texto_lower in p.get_name().lower()
            or texto_lower in p.get_vorname().lower()
        ]

        if not resultados:
            _label(self.result_frame, "Keine Übereinstimmungen.").pack(pady=20)
            return

        for p in resultados:
            self._tarjeta(p)

    def _tarjeta(self, p):
        card = ctk.CTkFrame(self.result_frame, fg_color=C["bg_card"], corner_radius=8,
                            cursor="hand2")
        card.pack(fill="x", padx=8, pady=4)

        info = (
            f"{p.get_name()}, {p.get_vorname()}   |   "
            f"Geb: {p.get_gebdatum()}  ({p.get_edad()} J.)   |   "
            f"Tel: {p.get_telefono() or '—'}   |   "
            f"Zugang: {p.get_systemzugang()}"
        )
        info_lbl = _label(card, info)
        info_lbl.pack(side="left", padx=14, pady=12)
        info_lbl.configure(cursor="hand2")

        def seleccionar(event=None, patient=p, frame=card):
            # Deselecciona la anterior
            if self._selected_card and self._selected_card.winfo_exists():
                self._selected_card.configure(fg_color=C["bg_card"])
            # Selecciona la nueva
            frame.configure(fg_color=C["hover"])
            self._selected_card = frame
            self.app.seleccionar(patient)

        card.bind("<Button-1>", seleccionar)
        info_lbl.bind("<Button-1>", seleccionar)


# ── Vista: Lista completa ─────────────────────────────────────

class ListaFrame(ctk.CTkFrame):

    COLS = [
        ("Name",    "get_name",          115),
        ("Vorname", "get_vorname",        130),
        ("Geb.",    "get_gebdatum",        85),
       # ("Alter",   "get_edad",            48),
        ("Telefon", "get_telefono",       100),
        ("E-Mail",  "get_email",          130),
        ("Adresse", "get_direccion",      160),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=C["bg_main"])
        self.app = app
        self._selected_row = None    # frame de la fila seleccionada
        self._selected_bg  = None   # color original de esa fila (para restaurar)
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 6))
        _label(header, "Patientenliste", bold=True).pack(side="left")
        self.count_lbl = _label(header, "", small=True)
        self.count_lbl.pack(side="right")

        cols_bar = ctk.CTkFrame(self, fg_color=C["bg_panel"], corner_radius=8, height=38)
        cols_bar.pack(fill="x", padx=24)
        cols_bar.pack_propagate(False)
        for txt, _, w in self.COLS:
            ctk.CTkLabel(cols_bar, text=txt, font=config.FONT_BOLD,
                         text_color=C["acento"], width=w, anchor="w").pack(side="left", padx=4)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg_main"], corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(4, 16))

    def refresh(self):
        self._selected_row = None
        self._selected_bg  = None
        self.app.deseleccionar()

        for w in self.scroll.winfo_children():
            w.destroy()

        lista = self.app.patienten_list
        self.count_lbl.configure(text=f"{len(lista)} Patienten")

        if not lista:
            _label(self.scroll, "Die Liste ist leer.").pack(pady=30)
            return

        for i, p in enumerate(lista):
            bg  = C["bg_card"] if i % 2 == 0 else C["bg_panel"]
            row = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=6,
                               height=40, cursor="hand2")
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            for _, getter, w in self.COLS:
                valor = str(getattr(p, getter)())
                lbl = ctk.CTkLabel(row, text=valor, width=w, anchor="w",
                                   font=config.FONT_NORMAL, text_color=C["texto"],
                                   cursor="hand2")
                lbl.pack(side="left", padx=4)
                lbl.bind("<Button-1>", lambda e, patient=p, frame=row, orig=bg:
                         self._seleccionar(patient, frame, orig))
                lbl.bind("<Double-Button-1>", lambda e, patient=p:
                         VerVentana(self.app, patient))

            row.bind("<Button-1>", lambda e, patient=p, frame=row, orig=bg:
                     self._seleccionar(patient, frame, orig))
            row.bind("<Double-Button-1>", lambda e, patient=p:
                     VerVentana(self.app, patient))

    def _seleccionar(self, patient, frame, orig_bg):
        # Restaura color de fila anterior
        if self._selected_row and self._selected_row.winfo_exists():
            self._selected_row.configure(fg_color=self._selected_bg)
            for child in self._selected_row.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.configure(text_color=C["texto"])

        # Si click en la misma fila → deselecciona
        if self._selected_row is frame:
            self._selected_row = None
            self._selected_bg  = None
            self.app.deseleccionar()
            return

        # Selecciona nueva fila
        frame.configure(fg_color=C["acento"])
        # Pone texto oscuro para que se lea sobre el acento claro
        for child in frame.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.configure(text_color=C["bg_main"])

        self._selected_row = frame
        self._selected_bg  = orig_bg
        self.app.seleccionar(patient)
