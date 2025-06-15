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
    
    def serialize(self):
        d = {
            'mark' : self.mark,
            'model' : self.model,
            'matricule' : self.matricule,
            'capacity' : self.capacity
        }
        return d
    
    @classmethod
    def deserialize(cls, data : dict):
        return cls(
            mark = data['mark'],
            model = data['model'],
            matricule = data['matricule'],
            capacity = data['capacity']
        )