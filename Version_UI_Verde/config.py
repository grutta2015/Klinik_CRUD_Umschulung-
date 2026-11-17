# config.py — Zentrale Konfiguration für Farben, Schriften und UI-Konstanten
# Paletten: 1=Klinik Blau, 2=Warmes Grau, 3=Stahlgrau, 4=Salbei Grün
# Palettenwechsel: AKTIVE_PALETTE auf 1, 2, 3 oder 4 setzen

AKTIVE_PALETTE = 4  # ← hier die Palette wechseln (1 | 2 | 3 | 4)

# ─────────────────────────────────────────────────────────────
#  PALETTEN
# ─────────────────────────────────────────────────────────────

PALETTEN = {

    # ── 1: Klinik Blau ───────────────────────────────────────
    1: {
        "name": "Klinik Blau",

        # Fenster & Frame
        "FENSTER_BG":           "#EAF2FB",
        "FRAME_BG":             "#C5D8ED",
        "FRAME_CORNER_RADIUS":  12,

        # Texte
        "TITEL_FARBE":          "#1A2E4A",
        "LABEL_FARBE":          "#1A2E4A",
        "ID_FARBE":             "#2E6DA4",
        "FEHLER_FARBE":         "#C0392B",

        # Eingabefelder
        "ENTRY_BG":             "#FFFFFF",
        "ENTRY_TEXT":           "#1A2E4A",
        "ENTRY_BORDER":         "#2E6DA4",

        # Buttons – primär (Speichern, Bearbeiten, Nav)
        "BTN_PRIM_BG":          "#898989",
        "BTN_PRIM_TEXT":        "#333333",

        # Buttons – destruktiv (Löschen)
        "BTN_DEL_BG":           "#E05252",
        "BTN_DEL_TEXT":         "#131313",

        # Buttons – neutral (Neu)
        "BTN_NEU_BG":           "#898989",
        "BTN_NEU_TEXT":         "#333333",

        # Bestätigung / Erfolg (label_error grün)
        "BESTAETIGUNG_FARBE":   "#1A6B3A",
    },

    # ── 2: Warmes Grau ────────────────────────────────────────
    2: {
        "name": "Warmes Grau",

        "FENSTER_BG":           "#F5F2EE",
        "FRAME_BG":             "#D9D3CC",
        "FRAME_CORNER_RADIUS":  12,

        "TITEL_FARBE":          "#3A3530",
        "LABEL_FARBE":          "#3A3530",
        "ID_FARBE":             "#7A6F65",
        "FEHLER_FARBE":         "#C0513A",

        "ENTRY_BG":             "#FDFAF7",
        "ENTRY_TEXT":           "#3A3530",
        "ENTRY_BORDER":         "#7A6F65",

        "BTN_PRIM_BG":          "#898989",
        "BTN_PRIM_TEXT":        "#333333",

        "BTN_DEL_BG":           "#C0513A",
        "BTN_DEL_TEXT":         "#FFFFFF",

        "BTN_NEU_BG":           "#898989",
        "BTN_NEU_TEXT":         "#333333",

        "BESTAETIGUNG_FARBE":   "#3A6B45",
    },

    # ── 3: Stahlgrau ─────────────────────────────────────────
    3: {
        "name": "Stahlgrau",

        "FENSTER_BG":           "#EBEBEB",
        "FRAME_BG":             "#C9C5C5",
        "FRAME_CORNER_RADIUS":  12,

        "TITEL_FARBE":          "#2B2B2B",
        "LABEL_FARBE":          "#2B2B2B",
        "ID_FARBE":             "#555555",
        "FEHLER_FARBE":         "#B22222",

        "ENTRY_BG":             "#F7F7F7",
        "ENTRY_TEXT":           "#2B2B2B",
        "ENTRY_BORDER":         "#888888",

        "BTN_PRIM_BG":          "#898989",
        "BTN_PRIM_TEXT":        "#333333",

        "BTN_DEL_BG":           "#EF6767",
        "BTN_DEL_TEXT":         "#131313",

        "BTN_NEU_BG":           "#898989",
        "BTN_NEU_TEXT":         "#333333",

        "BESTAETIGUNG_FARBE":   "#2E6B2E",
    },

    # ── 4: Salbei Grün ────────────────────────────────────────
    4: {
        "name": "Salbei Grün",

        "FENSTER_BG":           "#F0F5F0",
        "FRAME_BG":             "#C8D8C8",
        "FRAME_CORNER_RADIUS":  12,
        "SIDEBAR_BG":          "#A8C8A8",

        "TITEL_FARBE":          "#2E4A3A",
        "LABEL_FARBE":          "#2E4A3A",
        "ID_FARBE":             "#4A7A5A",
        "FEHLER_FARBE":         "#C0513A",

        "ENTRY_BG":             "#F8FAF8",
        "ENTRY_TEXT":           "#2E4A3A",
        "ENTRY_BORDER":         "#4A7A5A",

        "BTN_PRIM_BG":          "#898989",
        "BTN_PRIM_TEXT":        "#333333",

        "BTN_DEL_BG":           "#C0513A",
        "BTN_DEL_TEXT":         "#FFFFFF",

        "BTN_NEU_BG":           "#898989",
        "BTN_NEU_TEXT":         "#333333",

        "BESTAETIGUNG_FARBE":   "#2E6B45",
    },
}

# ─────────────────────────────────────────────────────────────
#  SCHRIFT
# ─────────────────────────────────────────────────────────────

SCHRIFT_TITEL_GROESSE  = 16
SCHRIFT_TITEL_GEWICHT  = "bold"
SCHRIFT_BTN_GROESSE    = 14

# ─────────────────────────────────────────────────────────────
#  FENSTER
# ─────────────────────────────────────────────────────────────

FENSTER_TITEL    = "Patientenakte"
FENSTER_BREITE   = 1000
FENSTER_HOEHE    = 700
APPEARANCE_MODE  = "light" # Esta función controla el tema global de la interfaz.
                           # Las opciones son "light", "dark" o "system".
SIDEBAR_BREITE   = 200




# ─────────────────────────────────────────────────────────────
#  BUTTON-ABMESSUNGEN
# ─────────────────────────────────────────────────────────────

BTN_NAV_BREITE   = 70
BTN_STD_BREITE   = 100

# ─────────────────────────────────────────────────────────────
#  ENTRY-FELDER
# ─────────────────────────────────────────────────────────────

ENTRY_BREITE     = 180
GEBDATUM_HINT    = "DD.MM.YYYY"

# ─────────────────────────────────────────────────────────────
#  HILFSFUNKTION — aktive Palette laden
# ─────────────────────────────────────────────────────────────

def get_palette():
    """Gibt das Dictionary der aktuell aktiven Palette zurück."""
    return PALETTEN[AKTIVE_PALETTE]
