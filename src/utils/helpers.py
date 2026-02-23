import unicodedata, re
from datetime import datetime

PLATAFORMAS = {
    "PlayStation 4": ["ps4", "playstation4", "playstation 4", "playstation-4", "play station4", "play station 4", "play station-4"],
    "PlayStation 5": ["ps5", "playstation5", "playstation 5", "playstation-5", "play station5", "play station 5", "play station-5"]
}

FILTRO = ["ps4", "playstation4", "playstation 4", "playstation-4", "play station4", "play station 4", "play station-4",
          "ps5", "playstation5", "playstation 5", "playstation-5", "play station5", "play station 5", "play station-5",
          "edicao padrao", "padrao", "edicao standard", "edition standard", "standard edition", "standardedition", 
          "physical edition", "midia fisica", "wireless", "controller", 
          "jogo", "video game", "compativel com", "playstation", "hits", " -", "- "]

BLACK_LIST = ["suporte", "ventoinha", "base", "grip", "joystick", "silicone", "carregador", "carregamento", "limpeza", "protector",
              "capa", "protetora", "usb", "transporte", "card", "charging", "carrying", "reposicao", "botoes", "thumbsticks",
              "gaming", "paddles", "replacement", "cabo", "cooler", "estojo", "waterproof", "armazenamento", "display", "buttons "]

def remover_duplicatas(produtos):
    menores = {}

    for p in produtos:
        chave = (p["nome"], p["plataforma"])

        if chave not in menores or p["preco"] < menores[chave]["preco"]:
            menores[chave] = p

    return list(menores.values())

def normalizar(texto):
    '''a-z, 0-9, espaço, -'''
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    return texto

def tratar_nome(texto_nome):
    nome_tratado = normalizar(texto_nome)
    
    for v in FILTRO:
        padrao = r"\b" + re.escape(v) + r"\b"
        nome_tratado = re.sub(padrao, "", nome_tratado)

    nome_tratado = " ".join(nome_tratado.split())

    if nome_tratado.endswith("-"):
        nome_tratado = nome_tratado[:-1].strip()

    for palavra in BLACK_LIST:
        if palavra in nome_tratado:
            return None

    return nome_tratado

def tratar_plataforma(texto_plataforma, texto_nome):
    if texto_plataforma == "Sem Sistema Operacional":
        nome_tratado = normalizar(texto_nome)
        for plataforma, valores in PLATAFORMAS.items():
            for v in valores:
                if v in nome_tratado:
                    return plataforma
        return texto_plataforma
    elif texto_plataforma == "PlayStation 4" or texto_plataforma == "PlayStation 5":
        return texto_plataforma
    else:
        return None
    
def tratar_key(texto_nome, texto_plataforma, texto_loja):
    if not texto_nome or not texto_plataforma or not texto_loja:
        return None
    else:
        return f"{texto_nome}_{texto_plataforma}_{texto_loja}"

def tratar_preco(texto_preco):
    try:
        # Mantém apenas numeros e virgula
        limpo = re.sub(r"[^0-9,]", "", texto_preco)
        return float(limpo.replace(",", "."))
    except ValueError:
        return False
    
def tratar_updated():
    data = datetime.now()
    data_formatada = data.strftime("%d/%m/%Y %H:%M:%S")
    return data_formatada
