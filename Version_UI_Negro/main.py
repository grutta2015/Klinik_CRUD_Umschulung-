"""
main.py
Punto de entrada de Klinik 2001.
Solo conecta las piezas: inicializa DB, carga datos, arranca UI.
"""

import database
import ui


def main():
    database.inicializar()
    patienten_list = database.load()

    app = ui.App(patienten_list)
    app.mainloop()

    database.cerrar()


if __name__ == "__main__":
    main()
