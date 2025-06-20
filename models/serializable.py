from abc import abstractmethod, ABC

class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data : dict) -> object:
        pass