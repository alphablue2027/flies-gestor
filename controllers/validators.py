from ..src.gestor import FliesGestor

def is_name_valid(*name : str) -> bool:
    for i in name:
        for j in i.split():
            if not j.isalpha():
                return False
    return True

def is_name_exist(name : str) -> bool:
    if list(filter(lambda a : a.name == name, FliesGestor.get_airlines())):
        return False
    return True

def is_fcode_valid(code : str, acode : str) -> bool:
    if not (len(code) >= 3 and code[:2] == acode and code[2:].isdigit()):
        return False
    return True

def is_fcode_exist(code : str) -> bool:
    if list(filter(lambda f : f.code == code, FliesGestor.get_nationals() + FliesGestor.get_internationals())):
        return False
    return True

def is_acode_valid(code : str) -> bool:
    if not (len(code) == 2 and code.isalpha()):
        return False
    return True

def is_acode_exist(code : str) -> bool:
    if list(filter(lambda a : a.code == code, FliesGestor.get_airlines())):
        return False
    return True

def is_mm_valid(*text : str) -> bool:
    for i in text:
        if not (len(i) >= 3 and i.isalnum() and i.isascii()):
            return False
    return True