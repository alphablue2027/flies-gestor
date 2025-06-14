from .serializable import Serializable

class Airline(Serializable):
    def __init__(self, name : str, code : str, planes_number : int, nationality : str):
        self._name = name
        self._code = code
        self._planes_number = planes_number
        self._nationality = nationality
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        self._code = value
    
    @property
    def planes_number(self):
        return self._planes_number
    
    @planes_number.setter
    def planes_number(self, value):
        self._planes_number = value
    
    @property
    def nationality(self):
        return self._nationality
    
    @nationality.setter
    def nationality(self, value):
        self._nationality = value
    
    def serialize(self):
        d = {
            'name' : self.name,
            'code' : self.code,
            'planes_number' : self.planes_number,
            'nationality' : self.nationality
        }
        return d

    @classmethod
    def deserialize(cls, data : dict):
        return cls(
            code = data['code'],
            name = data['name'],
            nationality = data['nationality'],
            planes_number = data['planes_number']
        )