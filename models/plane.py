# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from .serializable import Serializable

class Plane(Serializable):
    def __init__(self, mark : str, model : str, matricule : str, capacity : int):
        self._mark = mark
        self._model = model
        self._matricule = matricule
        self._capacity = capacity
    
    @property
    def mark(self):
        return self._mark
    
    @mark.setter
    def mark(self, value : str):
        self._mark = value
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value : str):
        self._model = value
    
    @property
    def matricule(self):
        return self._matricule
    
    @matricule.setter
    def matricule(self, value : str):
        self._matricule = value
    
    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value : int):
        self._capacity = value
    
    def serialize(self) -> dict:
        return {
            'mark' : self.mark,
            'model' : self.model,
            'matricule' : self.matricule,
            'capacity' : self.capacity
        }
    
    @classmethod
    def deserialize(cls, data : dict) -> object:
        return cls(
            mark = data['mark'],
            model = data['model'],
            matricule = data['matricule'],
            capacity = data['capacity']
        )