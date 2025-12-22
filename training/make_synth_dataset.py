import json
from pathlib import Path
import random

# Protocolos internos (exemplo sintético)
PROTOCOLS = [
    {
        "id": "HAS_001",
        "title": "Hipertensão Arterial (educativo)",
        "content": (
            "Hipertensão pode ser assintomática. Confirmar com medições repetidas. "
            "Mudanças de estilo de vida ajudam: reduzir sal, manter peso saudável, atividade física, "
            "evitar tabaco e moderar álcool. Em sinais de gravidade, procurar urgência."
        )
    },
    {
        "id": "DOR_TORACICA_001",
        "title": "Dor torácica (alerta)",
        "content": (
            "Dor no peito com falta de ar, sudorese, desmaio, fraqueza súbita ou irradiação "
            "é sinal de alerta e requer atendimento imediato."
        )
    }
]

def gen_example():
    prot = random.choice(PROTOCOLS)
    case = random.choice([
        "Paciente relata pressão 150x95 em medições repetidas, sem sintomas importantes.",
        "Paciente com dor no peito e falta de ar iniciados há 30 minutos.",
        "Paciente com tontura ocasional e pressão elevada recente."
    ])
    question = random.choice([
        "Quais orientações gerais devo passar?",
        "Quais sinais de alerta devo observar?",
        "Qual deve ser o próximo passo com segurança?"
    ])

    inp = f"PROTOCOLO: {prot['title']}\nCASO: {case}\nPERGUNTA: {question}"
    out = (
        "1) Resumo do caso\n"
        f"- {case}\n\n"
        "2) Orientação geral\n"
        "- Orientações educativas e seguras, sem diagnóstico e sem prescrição.\n"
        f"- Baseado no protocolo interno: {prot['id']}.\n\n"
        "3) Sinais de alerta\n"
        "- Se houver piora importante, sintomas intensos ou sinais de gravidade, buscar urgência.\n\n"
        "4) Próximos passos\n"
        "- Confirmar dados, acompanhar sinais e encaminhar para avaliação profissional.\n"
        f"Fonte: {prot['id']} ({prot['title']})."
    )
    return {"input": inp, "output": out, "source_id": prot["id"]}

def write_jsonl(path: str, n: int):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for _ in range(n):
            f.write(json.dumps(gen_example(), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    write_jsonl("data/raw/train.jsonl", 300)
    write_jsonl("data/raw/val.jsonl", 60)
    # salva protocolos para RAG
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    with Path("data/raw/protocols.json").open("w", encoding="utf-8") as f:
        json.dump(PROTOCOLS, f, ensure_ascii=False, indent=2)
    print("OK: dataset sintético + protocolos gerados.")
