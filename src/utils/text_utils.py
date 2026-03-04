import unicodedata, re
from utils.constants import REMOVER_EXPRESSOES, REMOVER_PALAVRAS, REMOVER_PALAVRAS_BORDA, BLACKLIST_EXPRESSOES, BLACKLIST_PALAVRAS

def normalizar(texto):
    '''a-z, 0-9, espaço'''
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto) # une multiplos espaços
    return texto

def remover_expressoes(texto):
    for exp in REMOVER_EXPRESSOES:
        padrao = rf"\b{re.escape(exp)}\b"
        texto = re.sub(padrao, "", texto)
    return re.sub(r"\s+", " ", texto).strip()

def remover_palavras(texto):
    palavras = texto.split()
    palavras_filtradas = [
        p for p in palavras if p not in REMOVER_PALAVRAS
    ]
    texto_limpo = " ".join(palavras_filtradas)
    return re.sub(r"\s+", " ", texto_limpo).strip()

def remover_palavras_borda(texto):
    palavras = texto.split()

    while palavras and palavras[0] in REMOVER_PALAVRAS_BORDA:
        palavras.pop(0)
        
    while palavras and palavras[-1] in REMOVER_PALAVRAS_BORDA:
        palavras.pop()
        
    return " ".join(palavras)

def contem_blacklist_expressoes(texto):
    for exp in BLACKLIST_EXPRESSOES:
        padrao = rf"\b{re.escape(exp)}\b"
        if re.search(padrao, texto):
            return True
    return False

def contem_blacklist_palavras(texto):
    palavras = texto.split()
    return any(p in BLACKLIST_PALAVRAS for p in palavras)

def contem_blacklist(texto):
    return (
        contem_blacklist_expressoes(texto)
        or contem_blacklist_palavras(texto)
    )
