import datenbank
import ui

if __name__ == "__main__":
    datenbank.inicializar()
    ui.root.mainloop()
    datenbank.cerrar()


# Cuando Python ejecuta un archivo directamente, 
# la variable __name__ vale "__main__". 
# Si ese archivo es importado por otro, __name__ vale 
# el nombre del módulo — y el bloque no se ejecuta. 
# Es una guardia para que el código de arranque 
# solo corra cuando tú lo lanzas explícitamente.

# Orden de arranque que quedaría:
# main.py
#   → datenbank.inicializar()
#   → ui.root.mainloop()   ← abre la ventana, todo funciona
#   → datenbank.cerrar()   ← cuando cierras la ventana