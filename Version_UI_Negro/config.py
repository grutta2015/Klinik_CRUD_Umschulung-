"""
config.py
Todas las constantes visuales de la aplicación.
Para cambiar de paleta, edita solo PALETA_ACTIVA.
"""

# ── Paletas ───────────────────────────────────────────────────

PALETAS = {
    "ceniza": {
        "bg_main":    "#1a1a1a",   # ventana principal
        "bg_panel":   "#2c2c2c",   # paneles / sidebar
        "bg_card":    "#3e3e3e",   # tarjetas / frames internos
        "acento":     "#a89f94",   # botones, bordes activos, texto destacado
        "texto":      "#e0e0e0",   # texto principal
        "texto_suave":"#888888",   # texto secundario / placeholders
        "borde":      "#3e3e3e",   # bordes de widgets
        "hover":      "#4a4a4a",   # hover de botones y filas
        "danger":     "#c0776a",   # rojo suave para errores / borrar
    },
    "marron": {
        "bg_main":    "#1c1410",
        "bg_panel":   "#2e2018",
        "bg_card":    "#4a3728",
        "acento":     "#b89a7a",
        "texto":      "#e8ddd0",
        "texto_suave":"#8a7a6a",
        "borde":      "#4a3728",
        "hover":      "#5a4535",
        "danger":     "#c0776a",
    },
    "hibrida": {
        "bg_main":    "#1a1a1a",   # gris de Ceniza como base
        "bg_panel":   "#2e2018",   # panel cálido de Marrón
        "bg_card":    "#3e3530",   # mezcla intermedia
        "acento":     "#b89a7a",   # acento cálido de Marrón
        "texto":      "#e8ddd0",
        "texto_suave":"#8a8078",
        "borde":      "#4a3e35",
        "hover":      "#4a4035",
        "danger":     "#c0776a",
    },
    "bosque": {
        "bg_main":    "#0f1410",
        "bg_panel":   "#1a2218",
        "bg_card":    "#2d3d2a",
        "acento":     "#82a87e",
        "texto":      "#d8e8d5",
        "texto_suave":"#6a886a",
        "borde":      "#2d3d2a",
        "hover":      "#3a4e36",
        "danger":     "#c0776a",
    },
}

# ── Paleta activa ─────────────────────────────────────────────
# Opciones: "ceniza" | "marron" | "hibrida" | "bosque"
PALETA_ACTIVA = "ceniza"

# Acceso rápido — el resto de la app importa solo `C`
C = PALETAS[PALETA_ACTIVA]


# ── Tipografía ────────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"
FONT_NORMAL  = (FONT_FAMILY, 13)
FONT_BOLD    = (FONT_FAMILY, 13, "bold")
FONT_TITLE   = (FONT_FAMILY, 18, "bold")
FONT_SMALL   = (FONT_FAMILY, 11)

# ── Dimensiones ───────────────────────────────────────────────
VENTANA_W    = 1000
VENTANA_H    = 660
SIDEBAR_W    = 200
CORNER_R     = 8      # border-radius general de customtkinter

# ── App ───────────────────────────────────────────────────────
APP_NOMBRE   = "Klinik 2001"
APP_VERSION  = "2.0"
