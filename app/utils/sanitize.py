def escape_markdown_v2(text: str) -> str:
    replacements: dict[str, str] = {
        "\\": "\\\\",  # Escapar barra invertida
        "_": "\\_",  # Escapar sublinhado
        "*": "\\*",  # Escapar asterisco
        "[": "\\[",  # Escapar colchete aberto
        "]": "\\]",  # Escapar colchete fechado
        "(": "\\(",  # Escapar parêntese aberto
        ")": "\\)",  # Escapar parêntese fechado
        "~": "\\~",  # Escapar til
        ">": "\\>",  # Escapar sinal de maior
        "#": "\\#",  # Escapar cerquilha
        "+": "\\+",  # Escapar mais
        "-": "\\-",  # Escapar menos
        "=": "\\=",  # Escapar igual
        "|": "\\|",  # Escapar barra vertical
        "{": "\\{",  # Escapar chave aberta
        "}": "\\}",  # Escapar chave fechada
        ".": "\\.",  # Escapar ponto
        "`": "\\`",  # Escapar crase
        "!": "\\!",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def real_to_float(reais):
    reais = reais.replace("R$", "").strip()

    if "," in reais:
        reais = reais.replace(".", "").replace(",", ".")

    return float(reais)
