import re
from datetime import datetime
from utils.text_utils import normalizar, contem_blacklist, remover_expressoes, remover_palavras, remover_palavras_borda
from utils.constants import PLATAFORMAS

def tratar_nome(texto_nome):
    nome_normalizado = normalizar(texto_nome)
    if contem_blacklist(nome_normalizado): return None
    nome_sem_expressoes = remover_expressoes(nome_normalizado)
    nome_filtrado = remover_palavras(nome_sem_expressoes)
    nome_tratado = remover_palavras_borda(nome_filtrado)
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

def tratar_href(texto_href_cru, loja):
    match loja:
        case 1:
            identificador = "/".join(texto_href_cru.split('/')[2:4])
            texto_href = "https://www.amazon.com.br/" + identificador

        case 2:
            identificador = "/".join(texto_href_cru.split('/')[4:6])
            identificador = identificador.split('?')[0]
            texto_href = "https://www.mercadolivre.com.br/" + identificador

        case _:
            texto_href = "https://www.google.com"

    return texto_href

def tratar_url_imagem(texto_url_imagem_cru):
    texto_url_imagem = texto_url_imagem_cru
    return texto_url_imagem

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
