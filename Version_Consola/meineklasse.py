from datetime import datetime



class Person:

    __name = ''
    __vorname = ''
    __gebdatum = ''
    __systemzugang = ''
    __id = None
    # __alter = 0
    
    def __init__(self, name, vorname, gebdatum, systemzugang, id=None):
        self.set_id(id)
        self.set_name(name)
        self.set_vorname(vorname)
        self.set_gebdatum(gebdatum)
        self.set_systemzugang(systemzugang)
        # self.set_alter(alter)  
    
##--- Setters
    def set_id(self, id):
        # Solo intentamos convertir a int si id no es None
        if id is not None:
            self.__id = int(id)
        else:
            self.__id = None
    def set_name(self, name):                    
        self.__name = str(name)
    def set_vorname(self, vorname):                    
        self.__vorname = str(vorname)
    def set_gebdatum(self, gebdatum):                    
        self.__gebdatum = str(gebdatum)
    def set_systemzugang(self, systemzugang):                    
        self.__systemzugang = str(systemzugang) 
    # def set_alter(self, alter):
    #     self.__alter = int(alter)

##---- Getters
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_vorname(self):
        return self.__vorname
    def get_gebdatum(self):
        return self.__gebdatum
    def get_systemzugang(self):
        return self.__systemzugang
    

    # def get_alter(self):
    #     return self.__alter
    
    
    def get_edad(self):
        datum_heute = datetime.now()
        gebdatum = datetime.strptime(self.__gebdatum, "%d.%m.%Y")
        
        alter_patient = datum_heute.year - gebdatum.year
        # Resta 1 si aún no ha pasado el día del cumpleaños este año
        schon_geburstag = (datum_heute.month, datum_heute.day) < (gebdatum.month, gebdatum.day)
        if schon_geburstag:
            alter_patient -= 1
            
        return alter_patient

