# verschreibung_klasse.py
# Une un medicamento del vademecum con un paciente
# Mismo patrón que adresse_klasse.py

class Verschreibung:

    def __init__(self, medikamentID, frequenz, datum, verschreibungID=None):
        self.__medikamentID   = None   # referencia al medicamento en el vademecum ("MID0001")
        self.__frequenz       = ""     # ej: "2x täglich"
        self.__datum          = ""     # ej: "26.04.2026"
        self.__verschreibungID = None  # se asigna en datenbank.py ("VID0001")

        self.set_medikamentID(medikamentID)
        self.set_frequenz(frequenz)
        self.set_datum(datum)
        self.set_verschreibungID(verschreibungID)

    ##--- Setters

    def set_medikamentID(self, medikamentID):
        self.__medikamentID = medikamentID

    def set_frequenz(self, frequenz):
        self.__frequenz = str(frequenz)

    def set_datum(self, datum):
        self.__datum = str(datum)

    def set_verschreibungID(self, verschreibungID):
        self.__verschreibungID = verschreibungID

    ##--- Getters

    def get_medikamentID(self):    return self.__medikamentID
    def get_frequenz(self):        return self.__frequenz
    def get_datum(self):           return self.__datum
    def get_verschreibungID(self): return self.__verschreibungID
