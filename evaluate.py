from assistant.chain import criar_chain, executar

CASOS = [
    "Paciente com febre há 3 dias, cansaço e dor no corpo.",
    "Paciente com dor no peito e falta de ar iniciados há 30 minutos.",
    "Paciente com pressão 150x95 em medições repetidas, sem sintomas.",
]

def checar_formato(txt: str) -> dict:
    t = txt.lower()
    return {
        "tem_resumo": "resumo" in t,
        "tem_orientacao": "orientação" in t or "orientacao" in t,
        "tem_alerta": "sinais de alerta" in t or "alerta" in t,
        "tem_proximos_passos": "próximos passos" in t or "proximos passos" in t,
        "nao_diagnostica": "diagnóstico" in t or "diagnostico" in t,  # só pra inspecionar
        "tamanho": len(txt),
    }

if __name__ == "__main__":
    chain = criar_chain()

    for i, caso in enumerate(CASOS, start=1):
        print("\n" + "="*80)
        print(f"CASO {i}: {caso}")
        resp = executar(chain, caso)
        print("\nRESPOSTA:\n", resp)

        m = checar_formato(resp)
        print("\nMÉTRICAS:", m)
