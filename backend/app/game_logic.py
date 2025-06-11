import random

PALAVRAS = ["SAGAZ", "AMAGO", "EXITO", "MEXER", "TERMO", "NOBRE", "SENSO", "AFETO", "PLENA", "ETICA", "MUTUA", "TENUE", "FAZER", "ASSIM", "VIGOR", "IDEIA", "PODER", "ANEXO", "GRATO", "GENRO"]

def escolher_palavra() -> str:
    """Retorna uma palavra aleatória da lista."""
    return random.choice(PALAVRAS)

def avaliar_tentativa(secreta: str, tentativa: str) -> list[str]:
    """
    Avalia a tentativa e retorna uma lista com os resultados.
    'V' = Verde (letra e posição corretas)
    'A' = Amarelo (letra correta, posição errada)
    'I' = Inexistente (letra não está na palavra)
    """
    feedback = [''] * 5
    secreta_lista = list(secreta)
    tentativa_lista = list(tentativa.upper())

    for i in range(5):
        if tentativa_lista[i] == secreta_lista[i]:
            feedback[i] = 'V'
            secreta_lista[i] = None
            tentativa_lista[i] = None

    for i in range(5):
        if tentativa_lista[i] is not None:
            if tentativa_lista[i] in secreta_lista:
                feedback[i] = 'A'
                secreta_lista[secreta_lista.index(tentativa_lista[i])] = None
            else:
                feedback[i] = 'I'
    
    return feedback