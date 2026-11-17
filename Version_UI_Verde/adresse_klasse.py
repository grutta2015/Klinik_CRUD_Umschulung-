class Adresse:

    def __init__(self, strasse, hausnummer, plz, ort, adresseID=None):
        self.__strasse = ""
        self.__hausnummer = ""
        self.__plz = ""
        self.__ort = ""
        self.__adresseID = None

        self.set_strasse(strasse)
        self.set_hausnummer(hausnummer)
        self.set_plz(plz)
        self.set_ort(ort)
        self.set_adresseID(adresseID)   
        # adresseID -> en  datenbank.py se hace(Format "AID0001")
        # como PID en Patient en datenbank.py se pone la ID

    ##--- Setters

    def set_strasse(self, strasse):
        self.__strasse = str(strasse)

    def set_hausnummer(self, hausnummer):
        self.__hausnummer = str(hausnummer)
    
    def set_plz(self, plz):
        self.__plz = str(plz)

    def set_ort(self, ort):
        self.__ort = str(ort)

    def set_adresseID(self, adresseID):
        # ID en datenbank.py se genera "AID0001"
        self.__adresseID = adresseID

    ##--- Getters

    def get_strasse(self):        return self.__strasse
    def get_hausnummer(self):     return self.__hausnummer
    def get_plz(self):            return self.__plz
    def get_ort(self):            return self.__ort      
    def get_adresseID(self):      return self.__adresseID