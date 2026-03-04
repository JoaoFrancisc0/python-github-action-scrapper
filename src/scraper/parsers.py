import logging
from utils.helpers import remover_duplicatas, tratar_nome, tratar_plataforma, tratar_href, tratar_url_imagem, tratar_preco, tratar_updated, tratar_key

def scrap_lista_produtos(page, paginas):
    page.screenshot(path="screenshot.png")
    paginas-=1
    resultados_total = []
    while(paginas > 0):
        resultados = parse_produtos_amazon(page, timeout=1000)
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

def parse_produtos_amazon(page, timeout):
    resultados = []
    
    try:
        page.wait_for_selector("[class='s-main-slot s-result-list s-search-results sg-row']", timeout=10000)
    except Exception:
        logging.warning("O container de resultados não foi encontrado a tempo.")
        return []

    items = page.locator("[role='listitem'][data-component-type='s-search-result']").all()
    
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
                # Depois tirar desse loop os atributos que serão repetidos para cada subitem
                try:
                    nome_cru = item.locator("h2 span").first.inner_text(timeout=timeout)
                except:
                    logging.error(f"Erro ao extrair nome")
                    raise
                try:
                    url_imagem_cru = item.locator("[class='s-image']").first.get_attribute("src")
                except:
                    logging.error(f"Erro ao extrair url_imagem")
                    raise
                try:
                    # Verifica se tem a Plataforma, se tiver pega o nome e o href, caso nao ele pega o href posteriormente
                    plataforma_element = sub_item.locator("[class='a-size-base a-link-normal s-underline-text s-underline-link-text null s-link-style a-text-bold']")
                    plataforma_cru = plataforma_element.inner_text(timeout=timeout)
                    href_cru = plataforma_element.get_attribute("href", timeout=timeout)
                except:
                    plataforma_cru = "Sem Sistema Operacional"
                    try:
                        href_cru = item.locator("[class='a-link-normal s-line-clamp-2 puis-line-clamp-3-for-col-4-and-8 s-link-style a-text-normal']").get_attribute("href", timeout=timeout)
                    except:
                        href_cru = ""
                try:
                    preco_cru = sub_item.locator("[class='a-offscreen']").first.inner_text(timeout=timeout)
                except:
                    logging.error(f"Erro ao extrair preco")
                    raise
                nome = tratar_nome(nome_cru)
                plataforma = tratar_plataforma(nome_cru, plataforma_cru)
                url_imagem = tratar_url_imagem(url_imagem_cru)
                loja = 1 # == "amazon"
                href = tratar_href(href_cru, loja)
                preco = tratar_preco(preco_cru)
                updated = tratar_updated()
                key = tratar_key(nome, plataforma, loja)
                
                if not key or not preco:
                    continue

                dados = {
                    "nome": nome,
                    "plataforma": plataforma,
                    "url_imagem": url_imagem,
                    "loja": loja,
                    "href": href,
                    "preco": preco,
                    "updated": updated,
                    "key": key
                }
                resultados.append(dados)
        except:
            continue
    logging.info(f"Produtos coletados na página: {len(resultados)}")
    return resultados

def scrap_lista_produtos_ml(page, paginas):
    page.screenshot(path="screenshot.png")
    paginas-=1
    resultados_total = []
    while(paginas > 0):
        resultados = parse_produtos_ml(page, timeout=1000)
        resultados_total.extend(resultados)
        if not avancar_pagina_ml(page):
            if not avancar_pagina_ml(page):
               return resultados_total
        paginas-=1
    resultado_tratado = remover_duplicatas(resultados_total)
    return resultado_tratado

def avancar_pagina_ml(page):
    try:
        button = page.locator("[data-andes-pagination-control='next']")
        button.click()
        return True
    except Exception as e:
        logging.error(f"Erro ao avançar página: {e}")
        return False

def parse_produtos_ml(page, timeout):
    resultados = []
    
    # try:
    #     page.wait_for_selector("[class='s-main-slot s-result-list s-search-results sg-row']", timeout=10000)
    # except Exception:
    #     logging.warning("O container de resultados não foi encontrado a tempo.")
    #     return []

    items = page.locator(".ui-search-layout__item").all()
    
    for item in items:
        try:
            try:
                nome_cru = item.locator(".poly-component__title").first.inner_text(timeout=timeout)
            except:
                logging.error(f"Erro ao extrair nome")
                raise
            try:
                url_imagem_cru = item.locator("[class='poly-component__picture']").first.get_attribute("src")
            except:
                logging.error(f"Erro ao extrair url_imagem")
                raise
            try:
                preco_cru = item.locator(".andes-money-amount__fraction").first.inner_text(timeout=timeout)
            except:
                logging.error(f"Erro ao extrair preco")
                raise

            try:
                href_cru = item.locator(".poly-component__title").first.get_attribute("href", timeout=timeout)
            except:
                href_cru = ""

            nome = tratar_nome(nome_cru)
            plataforma = tratar_plataforma(nome_cru)
            url_imagem = tratar_url_imagem(url_imagem_cru)
            loja = 2 # == "ml"
            href = tratar_href(href_cru, loja)
            preco = tratar_preco(preco_cru)
            updated = tratar_updated()
            key = tratar_key(nome, plataforma, loja)
            
            if not key or not preco:
                continue

            dados = {
                "nome": nome,
                "plataforma": plataforma,
                "url_imagem": url_imagem,
                "loja": loja,
                "href": href,
                "preco": preco,
                "updated": updated,
                "key": key
            }
            resultados.append(dados)
        except:
            continue
    logging.info(f"Produtos coletados na página: {len(resultados)}")
    return resultados
