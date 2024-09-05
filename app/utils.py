def escape_markdown_v2(text):
        replacements = {
            '\\': '\\\\',  # Escapar barra invertida
            '_': '\\_',    # Escapar sublinhado
            '*': '\\*',    # Escapar asterisco
            '[': '\\[',    # Escapar colchete aberto
            ']': '\\]',    # Escapar colchete fechado
            '(': '\\(',    # Escapar parêntese aberto
            ')': '\\)',    # Escapar parêntese fechado
            '~': '\\~',    # Escapar til
            '>': '\\>',    # Escapar sinal de maior
            '#': '\\#',    # Escapar cerquilha
            '+': '\\+',    # Escapar mais
            '-': '\\-',    # Escapar menos
            '=': '\\=',    # Escapar igual
            '|': '\\|',    # Escapar barra vertical
            '{': '\\{',    # Escapar chave aberta
            '}': '\\}',    # Escapar chave fechada
            '.': '\\.',    # Escapar ponto
            '`': '\\`',    # Escapar crase
            '!': '\\!',

        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
def converter_real_to_float(reais):
    if ',' in reais and '.' in reais:
        reais = reais.replace("R$", '').replace(".",'').strip()
        reais = reais.replace(",", '.')
    elif ',' in reais:
        reais = reais.replace("R$", '').replace(",",'.').strip()
    return float(reais)