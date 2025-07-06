# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from .flights import NationalFly, InternationalFly
from .airline import Airline
from datetime import date, datetime
import os
import json

class FilesGestor:
    def __init__(self):
        self.verify_files()
    
    def verify_files(self) -> bool:
        try:
            os.makedirs("./data/", exist_ok=True)
            return True
        except OSError:
            return False

    def __list_serializer(self, l : list) -> list:
        sl = list(map(lambda i : i.serialize(), l))
        return sl
    
    def save(self, nationals : list[NationalFly], internationals : list, airlines : list) -> bool:
        self.verify_files()
        nf = self.__list_serializer(nationals) 
        inf = self.__list_serializer(internationals)
        air = self.__list_serializer(airlines)
        try:
            with open("./data/nationals.json", 'w', encoding='utf-8') as file:
                json.dump(nf, file, indent=4, ensure_ascii=False)
            with open("./data/internationals.json", 'w', encoding='utf-8') as file:
                json.dump(inf, file, indent=4, ensure_ascii=False)
            with open("./data/airlines.json", 'w', encoding='utf-8') as file:
                json.dump(air, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(e)
            return False

    def read(self) -> tuple[list[NationalFly], list[InternationalFly], list[Airline]]:
        nationals = list()
        internationals = list()
        airlines = list()
        try:
            with open("./data/nationals.json", 'r', encoding='utf-8') as file:
                nationals = json.load(file, object_hook= NationalFly.deserialize)
            with open("./data/internationals.json", 'r', encoding='utf-8') as file:
                internationals = json.load(file, object_hook=InternationalFly.deserialize)
            with open("./data/airlines.json", 'r', encoding='utf-8') as file:
                airlines = json.load(file, object_hook= Airline.deserialize)
        except Exception as e:
            pass
        finally:
            return nationals, internationals, airlines


class FlightsGestor:
    __files = FilesGestor()
    __nationals, __internationals, __airlines = __files.read()
    
    @classmethod
    def get_nationals(cls) -> list[NationalFly]:
        return cls.__nationals
    
    @classmethod
    def get_internationals(cls) -> list[InternationalFly]:
        return cls.__internationals
    
    @classmethod
    def get_airlines(cls) -> list[Airline]:
        return cls.__airlines
    
    @classmethod
    def add_ifly(cls, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int, destiny : str, scale : bool, number : int):
        cls.__internationals.append(InternationalFly(code, inner, airline, init_city, end_city, datetime, mark, model, matr, capacity, destiny, scale, number))
    
    @classmethod
    def add_nfly(cls, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int):
        cls.__nationals.append(NationalFly(code, inner, airline, init_city, end_city, datetime, mark, model, matr, capacity))
    
    @classmethod
    def del_fly(cls, code: str) -> bool:
        finded = False
        for i in cls.get_nationals():
            if i.code == code.upper():
                cls.__nationals.remove(i)
                finded = True
        for i in cls.get_internationals():
            if i.code == code.upper():
                cls.__internationals.remove(i)
                finded = True
        return finded
    
    @classmethod
    def add_airline(cls, code : str, name : str, nation : str, planes : int):
        cls.__airlines.append(Airline(name, code, planes, nation))
        print(cls.__airlines)

    @classmethod
    def del_airline(cls, code : str) -> bool:
        finded = False
        for i in cls.__airlines:
            if i.code == code.upper():
                cls.__airlines.remove(i)
                finded = True
        cls.clean_links()
        return finded
    
    @classmethod
    def get_airline(cls, code : str) -> Airline | None:
        flights = cls.get_nationals() + cls.get_internationals()
        for i in flights:
            if i.code == code.upper():
                try:
                    return list(filter(lambda a : i.airline == a.name, cls.__airlines))[0]
                except IndexError:
                    pass
    
    @classmethod
    def get_airline_code(cls, name : str) -> str:
        return list(filter(lambda a : a.name == name, cls.__airlines))[0].code

    @classmethod
    def get_internationals_porcent(cls, mark : str, name : str) -> tuple[int, int, int]:
        flights = list(filter(lambda f : f.airline == name, cls.get_internationals()))
        c = len(list(filter(lambda f : f.plane.mark == mark, flights)))
        return c, len(flights), c*100//len(flights)
    
    @classmethod
    def get_passagers_avg(cls, destiny: str) -> tuple[int, list[InternationalFly]]:
        l = list(filter(lambda f: f.destiny == destiny, cls.get_internationals()))
        s = sum(list(map(lambda f : f.plane.capacity, l)))
        return s//len(l), l
    
    @classmethod
    def get_outers_nflights(cls, date: date) -> list[NationalFly]:
        flights = sorted(list(filter(lambda f : not f.inner and f.datetime.date() == date, cls.get_nationals())), key= lambda f: f.datetime.time())
        return flights
    
    @classmethod
    def get_scalest_fly(cls, date: date) -> InternationalFly | None:
        try:
            sf = sorted(list(filter(lambda f : not f.inner and f.datetime.date() == date, cls.get_internationals())), key= lambda f: f.scale_number, reverse=True)[0]
            return sf
        except Exception:
            return None
        
    @classmethod
    def clean_links(cls):
        air_names = list(map(lambda a : a.name, cls.__airlines))
        cls.__internationals = list(filter(lambda f : f.airline in air_names, cls.get_internationals()))
        cls.__nationals = list(filter(lambda f : f.airline in air_names, cls.get_nationals()))
    
    @classmethod
    def close(cls) -> bool:
        return cls.__files.save(cls.get_nationals(), cls.get_internationals(), cls.get_airlines())