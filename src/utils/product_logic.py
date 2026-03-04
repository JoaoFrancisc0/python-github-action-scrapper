def remover_duplicatas(produtos):
    menores = {}

    for p in produtos:
        chave = (p["nome"], p["plataforma"])

        if chave not in menores or p["preco"] < menores[chave]["preco"]:
            menores[chave] = p

    return list(menores.values())

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
