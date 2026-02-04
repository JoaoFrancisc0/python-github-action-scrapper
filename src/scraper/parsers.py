import logging
import re
from utils.helpers import normalizar
import time

PLATAFORMAS = {
    "PlayStation 4": ["ps4", "playstation4", "playstation 4", "playstation-4"],
    "PlayStation 5": ["ps5", "playstation5", "playstation 5", "playstation-5"]
}

FILTRO = ["ps4", "playstation4", "playstation 4", "playstation-4",
          "ps5", "playstation5", "playstation 5", "playstation-5",
          "edicao padrao", "edicao standard", "hits"]

def scrap_lista_produtos(page, paginas):
    paginas-=1
    resultados_total = []
    while(paginas > 0):
        resultados = parse_lista_produtos(page)
        resultados_total.extend(resultados)
        if not avancar_pagina(page):
            if not avancar_pagina(page):
               return resultados_total
        paginas-=1
    return resultados_total

def avancar_pagina(page):
    try:
        button = page.locator('xpath=//*[@role="button"  and normalize-space(text())="Próximo"]')
        button.click()
        return True
    except Exception as e:
        logging.error(f"Erro ao avançar página: {e}")
        return False

def parse_lista_produtos(page):
    """
    Extrai informações de múltiplos itens de uma página de listagem.
    """
    resultados = []
    
    # É uma boa prática esperar o seletor principal carregar antes de começar
    try:
        page.wait_for_selector("[class='s-main-slot s-result-list s-search-results sg-row']", timeout=10000)
    except Exception:
        logging.warning("O container de resultados não foi encontrado a tempo.")
        return []

    # Usamos locators (mais modernos e resilientes que query_selector)
    items = page.locator("[class='a-section a-spacing-small a-spacing-top-small']").all()
    
    for item in items:
        try:
            # Ignora anuncios patrocinados
            patrocinado = item.locator('xpath=.//div[@class="a-row a-spacing-micro"]//span[@class="a-declarative"]').first
            if patrocinado.is_visible():
                continue

            sub_items = []
            sub_items.append(item.locator("[data-cy='price-recipe']"))
            secondary_item = item.locator("[class='a-row a-spacing-mini']")
            if secondary_item.count() > 0:
                sub_items.append(secondary_item)

            for sub_item in sub_items:
                nome_cru = item.locator("h2 span").inner_text(timeout=2000)
                try:
                    plataforma_cru = sub_item.locator("[class='a-size-base a-link-normal s-underline-text s-underline-link-text null s-link-style a-text-bold']").inner_text(timeout=2000)
                except:
                    plataforma_cru = "Sem Sistema Operacional"
                preco_cru = sub_item.locator("[class='a-offscreen']").first.inner_text(timeout=2000)

                dados = {
                    "nome": limpar_nome(nome_cru),
                    "plataforma": limpar_plataforma(plataforma_cru, nome_cru),
                    "preco": limpar_preco(preco_cru),
                }
                
                if not dados["plataforma"]:
                    continue
                
                resultados.append(dados)
        except Exception as e:
            # Se um item falhar, logamos o erro mas continuamos para o próximo
            logging.error(f"Erro ao extrair dados de um item específico: {e}")
            continue
    return resultados

def limpar_nome(texto_nome):
    nome_tratado = normalizar(texto_nome)
    
    for v in FILTRO:
        padrao = r"\b" + re.escape(v) + r"\b"
        nome_tratado = re.sub(padrao, "", nome_tratado)

    nome_tratado = " ".join(nome_tratado.split())

    if nome_tratado.endswith("-"):
        nome_tratado = nome_tratado[:-1].strip()

    return nome_tratado

def limpar_plataforma(texto_plataforma, texto_nome):
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

def limpar_preco(texto_preco):
    try:
        # Mantém apenas numeros e virgula
        limpo = re.sub(r"[^0-9,]", "", texto_preco)
        return float(limpo.replace(",", "."))
    except ValueError:
        return False