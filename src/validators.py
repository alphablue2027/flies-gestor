from .gestor import FliesGestor

def is_text_valid(*text : str) -> bool:
    valid = True
    for i in text:
        if i == "":
            valid = False
    return valid

def is_name_valid(*name : str) -> bool:
    valid = True
    for i in name:
        if " " in i:
            for j in i.split():
                if not j.isalpha():
                    valid = False
        elif not i.isalpha():
            valid = False
    return valid

def is_aname_valid(name : str) -> bool:
    valid = True
    valid = is_name_valid(name)
    
    if list(filter(lambda a : a.name == name, FliesGestor.get_airlines())):
        valid = False
    return valid

def is_fcode_valid(code : str, acode : str) -> bool:
    valid = True
    if not (len(code) >= 3 and code[:2] == acode):
        valid = False
    elif not code[2:].isdigit():
        valid = False
    return valid

def is_fcode_exist(code : str) -> bool:
    if list(filter(lambda f : f.code == code, FliesGestor.get_nationals() + FliesGestor.get_internationals())):
        return False
    return True

def is_acode_valid(code : str) -> bool:
    valid = False
    if len(code) == 2 and code.isalpha():
        valid = True
    return valid

def is_acode_exist(code : str) -> bool:
    if list(filter(lambda a : a.code == code, FliesGestor.get_airlines())):
        return False
    return True

def is_mm_valid(*text : str) -> bool:
    valid = True
    for i in text:
        if not (len(i) >= 3 and i.isalnum() and i.isascii()):
            valid = False
    return valid