from .logging_conf import setup_logging
from .rag import build_vector_store
from .config import settings
from .graph import build_graph, AgentState

logger = setup_logging()

def main():
    print("Assistente Médico Virtual (Fase 3 - Nota 10)\n")
    build_vector_store(settings.CHROMA_DIR)
    graph = build_graph()

    while True:
        user = input("\nDescreva o caso (ou 'sair'): ").strip()
        if user.lower() == "sair":
            break

        st = AgentState(user_input=user)
        out = graph.invoke(st)

        print("\n--- RESPOSTA ---\n")
        print(out["answer"])
        print("\nFontes:", ", ".join(out.get("sources", [])))


if __name__ == "__main__":
    main()
