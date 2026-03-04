import unicodedata, re
from datetime import datetime

PLATAFORMAS = {
    "PlayStation-4": ["ps4", "playstation4", "playstation 4", "playstation-4", "play station4", "play station 4", "play station-4"],
    "PlayStation-5": ["ps5", "playstation5", "playstation 5", "playstation-5", "play station5", "play station 5", "play station-5"]
}

FILTRO = ["ps4", "playstation4", "playstation 4", "playstation-4", "play station4", "play station 4", "play station-4",
          "ps5", "playstation5", "playstation 5", "playstation-5", "play station5", "play station 5", "play station-5",
          "edicao padrao", "padrao", "edicao standard", "edition standard", "standard edition", "standardedition", 
          "physical edition", "midia fisica", "fisico", "lacrado", "wireless", "controller", 
          "jogo", "video game", "compativel com", "playstation", "hits", " -", "- ", "sony", 
          "pt-br", "pronta entrega"]

BLACK_LIST = ["suporte", "ventoinha", "base", "grip", "joystick", "silicone", "carregador", "carregamento", "limpeza", "protector",
              "capa", "protetora", "usb", "transporte", "card", "charging", "carrying", "reposicao", "botoes", "thumbsticks",
              "gaming", "paddles", "replacement", "cabo", "cooler", "estojo", "waterproof", "armazenamento", "display", "buttons",
              "nintendo", "ps3", "ps2", "psp", "xbox"]

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

def tratar_plataforma(texto_nome, texto_plataforma="Sem Sistema Operacional"):
    if texto_plataforma in PLATAFORMAS.get("PlayStation 4", []):
        return 4
    elif texto_plataforma in PLATAFORMAS.get("PlayStation 5", []):
        return 5
    # Tratamento para quando plataforma não é declarada
    else:
        nome_tratado = normalizar(texto_nome)
        for plataforma, valores in PLATAFORMAS.items():
            for v in valores:
                if v in nome_tratado:
                    if plataforma == "PlayStation 4":
                        return 4
                    elif plataforma == "PlayStation 5":
                        return 5
        return 1 # == "Sem Sistema Operacional"

def tratar_href(texto_href_cru, loja_url=""):
    texto_href = loja_url + texto_href_cru
    return texto_href

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

def comparar_preco(new_data, latest_prices):
    indice_antigo = {product["key"]: product["preco"] for product in latest_prices}

    alterados = []

    for product in new_data:
        key = product["key"]
        preco_novo = product["preco"]

        if key not in indice_antigo:
            alterados.append(product)

        else:
            preco_antigo = indice_antigo[key]
            if preco_antigo != preco_novo:
                alterados.append(product)

    return alterados
