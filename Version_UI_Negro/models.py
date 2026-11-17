from datetime import datetime


class Person:

    def __init__(self, name, vorname, gebdatum, systemzugang,
                 telefono="", email="", direccion="", id=None):
        self.__id        = None
        self.__name      = ""
        self.__vorname   = ""
        self.__gebdatum  = ""
        self.__systemzugang = ""
        self.__telefono  = ""
        self.__email     = ""
        self.__direccion = ""

        self.set_id(id)
        self.set_name(name)
        self.set_vorname(vorname)
        self.set_gebdatum(gebdatum)
        self.set_systemzugang(systemzugang)
        self.set_telefono(telefono)
        self.set_email(email)
        self.set_direccion(direccion)

    # ── Setters ──────────────────────────────────────────────
    def set_id(self, id):
        self.__id = int(id) if id is not None else None

    def set_name(self, name):
        self.__name = str(name)

    def set_vorname(self, vorname):
        self.__vorname = str(vorname)

    def set_gebdatum(self, gebdatum):
        self.__gebdatum = str(gebdatum)

    def set_systemzugang(self, systemzugang):
        self.__systemzugang = str(systemzugang)

    def set_telefono(self, telefono):
        self.__telefono = str(telefono)

    def set_email(self, email):
        self.__email = str(email)

    def set_direccion(self, direccion):
        self.__direccion = str(direccion)

    # ── Getters ──────────────────────────────────────────────
    def get_id(self):           return self.__id
    def get_name(self):         return self.__name
    def get_vorname(self):      return self.__vorname
    def get_gebdatum(self):     return self.__gebdatum
    def get_systemzugang(self): return self.__systemzugang
    def get_telefono(self):     return self.__telefono
    def get_email(self):        return self.__email
    def get_direccion(self):    return self.__direccion

    def get_edad(self):
        heute = datetime.now()
        geb   = datetime.strptime(self.__gebdatum, "%d.%m.%Y")
        alter = heute.year - geb.year
        if (heute.month, heute.day) < (geb.month, geb.day):
            alter -= 1
        return alter
