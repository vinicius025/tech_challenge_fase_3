import re

FORBIDDEN = [
    r"\b(dose|dosagem|mg|ml)\b",
    r"\b(tome|ingerir|prescrevo|prescrição)\b",
    r"\b(diagnóstico definitivo|você tem|isso é)\b",
]

def safety_check(text: str) -> tuple[bool, str]:
    low = text.lower()
    for pat in FORBIDDEN:
        if re.search(pat, low):
            return False, (
                "⚠️ Resposta ajustada para manter caráter educativo e seguro. "
                "Procure um profissional de saúde para avaliação. "
                "Se houver sinais de gravidade, busque atendimento imediato."
            )
    return True, text
