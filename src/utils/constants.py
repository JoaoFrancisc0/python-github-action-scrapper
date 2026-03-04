PLATAFORMAS = {
    "PlayStation 4": ["ps4", "playstation4", "playstation 4", "playstation-4", "play station4", "play station 4", "play station-4", "playstation_4"],
    "PlayStation 5": ["ps5", "playstation5", "playstation 5", "playstation-5", "play station5", "play station 5", "play station-5", "playstation_5"]
}

REMOVER_EXPRESSOES = ["playstation 4", "play station4", "play station 4",
                      "playstation 5", "play station5", "play station 5",
                      "edicao padrao", "edicao standard", "edition standard", "standard edition",
                      "midia fisica", "versao fisica", "edicao fisica", "physical edition",
                      "video game", "compativel com", "pronta entrega",
                      "com nf", "com nfe", "c nf", "c nfe"]

REMOVER_PALAVRAS = ["ps4, ps5",
                    "padrao", "standard",
                    "fisica", "fisico", "lacrado", "novo", "original"
                    "wireless", "controller", "jogo", "nf", "nfe",
                    "ubisoft", "ea", 
                    "playstation", "hits", "sony",
                    "portugues", "brasil", "ptbr", "br", 
                    "europeu", "europa", "euro", "eur",
                    "americano"]

REMOVER_PALAVRAS_BORDA = ["para", "for"]

BLACKLIST_EXPRESSOES = ["playstation 3", "playstation 2", "playstation 1", "ps vita"]

BLACKLIST_PALAVRAS = ["nintendo", "switch", "xbox", "ps3", "ps2", "ps1"]
