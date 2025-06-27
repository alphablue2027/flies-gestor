# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
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
    def name(self, value : str):
        self._name = value
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value : str):
        self._code = value
    
    @property
    def planes_number(self):
        return self._planes_number
    
    @planes_number.setter
    def planes_number(self, value : int):
        self._planes_number = value
    
    @property
    def nationality(self):
        return self._nationality
    
    @nationality.setter
    def nationality(self, value : str):
        self._nationality = value
    
    def serialize(self) -> dict:
        return {
            'name' : self.name,
            'code' : self.code,
            'planes_number' : self.planes_number,
            'nationality' : self.nationality
        }

    @classmethod
    def deserialize(cls, data : dict) -> object:
        return cls(
            code = data['code'],
            name = data['name'],
            nationality = data['nationality'],
            planes_number = data['planes_number']
        )