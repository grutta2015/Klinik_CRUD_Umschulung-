import datetime


class Medikamente:

    def __init__ (self, name, wirkstoff, dosis, frequenz, datum, medikamentID=None):
        self.__name = ""
        self.__wirkstoff = ""
        self.__dosis = 0.0
        self.__medikamentID = None
        self.__frequenz = (frequenz)  # Ejemplo: "3 veces al día"
        self.__datum = (datum)   

        self.set_name(name)
        self.set_wirkstoff(wirkstoff)
        self.set_dosis(dosis)
        self.set_medikamentID(medikamentID)
        self.set_frequenz(frequenz)
        self.set_datum(datum)
             # Ejemplo: "2026-04-25"

    ##--- Setters
    def set_name(self, name):
            self.__name = str(name)

    def set_wirkstoff(self, wirkstoff):
            self.__wirkstoff = str(wirkstoff)

    def set_dosis(self, dosis):
            self.__dosis = float(dosis)

    def set_medikamentID(self, medikamentID):
            self.__medikamentID = medikamentID

    def set_frequenz(self, frequenz):
        self.__frequenz = str(frequenz)

    def set_datum(self, datum=None):
        if datum is None:
            # Genera la fecha actual si no se recibe ninguna
            self.__datum = datetime.datetime.now().strftime("%d.%m.%Y")
        else:
            # Si se recibe una fecha (por ejemplo, desde el archivo), se respeta
            self.__datum = str(datum)
    
    ##--- Getters
    def get_name(self):         return self.__name
    def get_wirkstoff(self):    return self.__wirkstoff
    def get_dosis(self):        return self.__dosis
    def get_frequenz(self):     return self.__frequenz
    def get_datum(self):        return self.__datum
    def get_medikamentID(self): return self.__medikamentID
