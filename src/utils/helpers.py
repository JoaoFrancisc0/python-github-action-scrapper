import unicodedata
import re

def normalizar(texto):
    '''a-z, 0-9, espaço, -'''
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    return texto