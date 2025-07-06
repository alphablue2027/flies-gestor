# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from models.gestor import FlightsGestor

def is_name_valid(*name : str) -> bool:
    for i in name:
        for j in i.split():
            if not j.isalpha():
                return False
    return True

def is_name_exist(name : str) -> bool:
    if list(filter(lambda a : a.name == name, FlightsGestor.get_airlines())):
        return False
    return True

def is_fcode_valid(code : str, acode : str) -> bool:
    if not (len(code) >= 3 and code[:2] == acode and code[2:].isdigit()):
        return False
    return True

def is_fcode_exist(code : str) -> bool:
    if list(filter(lambda f : f.code == code, FlightsGestor.get_nationals() + FlightsGestor.get_internationals())):
        return False
    return True

def is_acode_valid(code : str) -> bool:
    if not (len(code) == 2 and code.isalpha()):
        return False
    return True

def is_acode_exist(code : str) -> bool:
    if list(filter(lambda a : a.code == code, FlightsGestor.get_airlines())):
        return False
    return True

def is_mm_valid(*text : str) -> bool:
    for i in text:
        if not (len(i) >= 3 and i.isalnum() and i.isascii()):
            return False
    return True