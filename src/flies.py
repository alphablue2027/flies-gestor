from .serializable import Serializable
from .plane import Plane
from datetime import datetime

class NationalFly(Serializable):
    def __init__(self, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int):
        self._code = code
        self._inner = inner
        self._airline = airline
        self._init_city = init_city
        self._end_city = end_city
        self._datetime = datetime
        self._plane = Plane(mark, model, matr, capacity)
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value : str):
        self._code = value
    
    @property
    def inner(self):
        return self._inner
    
    @inner.setter
    def inner(self, value : bool):
        self._inner = value

    @property
    def airline(self):
        return self._airline
    
    @airline.setter
    def airline(self, value : str):
        self._airline = value

    @property
    def init_city(self):
        return self._init_city
    
    @init_city.setter
    def init_city(self, value : str):
        self._init_city = value
    
    @property
    def end_city(self):
        return self._end_city
    
    @end_city.setter
    def end_city(self, value : str):
        self._end_city = value
    
    @property
    def datetime(self):
        return self._datetime
    
    @datetime.setter
    def datetime(self, value):
        self._datetime = value
    
    @property
    def plane(self):
        return self._plane
    
    @plane.setter
    def plane(self, value : Plane):
        self._plane = value
    
    def serialize(self):
        d = {
            'code' : self.code,
            'inner' : self.inner,
            'airline' : self.airline,
            'init_city' : self.init_city,
            'end_city' : self.end_city,
            'datetime' : self.datetime.strftime("%Y/%m/%d, %H:%M:%S"),
            'plane' : self.plane.serialize()
        }
        return d

    @classmethod
    def deserialize(cls, data : dict):
        if "mark" in data.keys():
            return Plane.deserialize(data)
        else:
            return cls (
                code = data['code'],
                inner = data['inner'],
                airline = data['airline'],
                init_city = data['init_city'],
                end_city = data['end_city'],
                datetime = datetime.strptime(data['datetime'], "%Y/%m/%d, %H:%M:%S"),
                mark = data['plane'].mark,
                model = data['plane'].model,
                matr = data['plane'].matricule,
                capacity = data['plane'].capacity
            )

class InternationalFly(NationalFly):
    def __init__(self, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int, destiny : str, scale : bool, scale_number : int):
        super().__init__(code, inner, airline, init_city, end_city, datetime, mark, model, matr, capacity)
        self._destiny = destiny
        self._scale = scale
        self._scale_number = scale_number
    
    @property
    def destiny(self):
        return self._destiny
    
    @destiny.setter
    def destiny(self, value):
        self._destiny = value
    
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
    
    @property
    def scale_number(self):
        return self._scale_number
    
    @scale_number.setter
    def scale_number(self, value):
        self._scale_number = value
    
    def serialize(self):
        d = super().serialize()
        d['destiny'] = self.destiny
        d['scale'] = self.scale
        d['scale_number'] = self.scale_number
        return d
    
    @classmethod
    def deserialize(cls, data : dict):
        if "mark" in data.keys():
            return Plane.deserialize(data)
        else:
            return cls(
                code = data['code'],
                inner = data['inner'],
                airline = data['airline'],
                init_city = data['init_city'],
                end_city = data['end_city'],
                datetime = datetime.strptime(data['datetime'], "%Y/%m/%d, %H:%M:%S"),
                mark = data['plane'].mark,
                model = data['plane'].model,
                matr = data['plane'].matricule,
                capacity = data['plane'].capacity,
                destiny = data['destiny'],
                scale = data['scale'],
                scale_number = data['scale_number']
            )