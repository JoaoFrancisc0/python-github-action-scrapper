import logging
from utils.helpers import remover_duplicatas, tratar_nome, tratar_plataforma, tratar_preco, tratar_updated, tratar_key

def scrap_lista_produtos(page, paginas):
    paginas-=1
    resultados_total = []
    while(paginas > 0):
        resultados = parse_lista_produtos(page, timeout=1000)
        resultados_total.extend(resultados)
        if not avancar_pagina(page):
            if not avancar_pagina(page):
               return resultados_total
        paginas-=1
    resultado_tratado = remover_duplicatas(resultados_total)
    return resultado_tratado

def avancar_pagina(page):
    try:
        button = page.locator('xpath=//*[@role="button"  and normalize-space(text())="Próximo"]')
        button.click()
        return True
    except Exception as e:
        logging.error(f"Erro ao avançar página: {e}")
        return False

def parse_lista_produtos(page, timeout):
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
                nome_cru = item.locator("h2 span").inner_text(timeout=timeout)
                try:
                    plataforma_cru = sub_item.locator("[class='a-size-base a-link-normal s-underline-text s-underline-link-text null s-link-style a-text-bold']").inner_text(timeout=timeout)
                except:
                    plataforma_cru = "Sem Sistema Operacional"
                preco_cru = sub_item.locator("[class='a-offscreen']").first.inner_text(timeout=timeout)

                nome = tratar_nome(nome_cru)
                plataforma = tratar_plataforma(plataforma_cru, nome_cru)
                preco = tratar_preco(preco_cru)
                updated = tratar_updated()
                loja = "amazon"
                key = tratar_key(nome, plataforma, loja)
                
                if not key or not preco:
                    continue

                dados = {
                    "nome": nome,
                    "plataforma": plataforma,
                    "loja": loja,
                    "preco": preco,
                    "updated": updated,
                    "key": key
                }
                
                resultados.append(dados)
        except Exception as e:
            # Se um item falhar, logamos o erro mas continuamos para o próximo
            logging.error(f"Erro ao extrair dados de um item específico: {e}")
            continue
    return resultados
