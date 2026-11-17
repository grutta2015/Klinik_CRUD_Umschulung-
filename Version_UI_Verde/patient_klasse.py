# patient_klasse.py
from datetime import datetime


class Patient:

    def __init__(self, name, vorname, gebdatum, systemzugang,
                 telefon="", email="", adresse_id=None, verschreibung_ids=None, id=None):
        self.__id                = None
        self.__name              = ""
        self.__vorname           = ""
        self.__gebdatum          = ""
        self.__systemzugang      = ""
        self.__telefon           = ""
        self.__email             = ""
        self.__adresse_id        = None  # un solo AID — ej: "AID0001"
        self.__verschreibung_ids = []    # lista de VIDs  — ej: ["VID0001", "VID0002"]
                                         # cada VID apunta a una Verschreibung en el archivo "verschreibungen"
                                         # la Verschreibung a su vez tiene el MID del medicamento del vademecum

        self.set_id(id)
        self.set_name(name)
        self.set_vorname(vorname)
        self.set_gebdatum(gebdatum)
        self.set_systemzugang(systemzugang)
        self.set_telefon(telefon)
        self.set_email(email)
        self.set_adresse_id(adresse_id)
        self.set_verschreibung_ids(verschreibung_ids)

    ##--- Setters

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = str(name)

    def set_vorname(self, vorname):
        self.__vorname = str(vorname)

    def set_gebdatum(self, gebdatum):
        self.__gebdatum = str(gebdatum)

    def set_systemzugang(self, systemzugang):
        self.__systemzugang = str(systemzugang)

    def set_telefon(self, telefon):
        self.__telefon = str(telefon)

    def set_email(self, email):
        self.__email = str(email)

    def set_adresse_id(self, adresse_id):
        self.__adresse_id = adresse_id

    def set_verschreibung_ids(self, verschreibung_ids):
        # None → [] para que siempre sea lista, nunca None
        if verschreibung_ids is None:
            self.__verschreibung_ids = []
        else:
            self.__verschreibung_ids = list(verschreibung_ids)

    # ── Vinculación — Verschreibung ───────────────────────────

    def add_verschreibung_id(self, verschreibungID: str):
        if verschreibungID not in self.__verschreibung_ids:
            self.__verschreibung_ids.append(verschreibungID)

    def remove_verschreibung_id(self, verschreibungID: str):
        if verschreibungID in self.__verschreibung_ids:
            self.__verschreibung_ids.remove(verschreibungID)

    ##--- Getters

    def get_id(self):                  return self.__id
    def get_name(self):                return self.__name
    def get_vorname(self):             return self.__vorname
    def get_gebdatum(self):            return self.__gebdatum
    def get_systemzugang(self):        return self.__systemzugang
    def get_telefon(self):             return self.__telefon
    def get_email(self):               return self.__email
    def get_adresse_id(self):          return self.__adresse_id
    def get_verschreibung_ids(self):   return self.__verschreibung_ids

    def get_alter(self):
        heute = datetime.now()
        geb   = datetime.strptime(self.__gebdatum, "%d.%m.%Y")
        alter = heute.year - geb.year
        if (heute.month, heute.day) < (geb.month, geb.day):
            alter -= 1
        return alter
