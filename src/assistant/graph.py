from dataclasses import dataclass, field
from typing import Any
from langgraph.graph import StateGraph, END
from .config import settings
from .logging_conf import setup_logging
from .rag import retrieve
from .safety import safety_check
from .llm_local import LocalLLM
from .llm_openai import make_openai_llm

logger = setup_logging()

ALERTA = ["dor no peito", "falta de ar", "desmaio", "fraqueza súbita", "confusão", "convuls"]

@dataclass
class AgentState:
    user_input: str
    urgency: bool = False
    contexts: list[dict[str, Any]] = field(default_factory=list)
    answer: str = ""
    sources: list[str] = field(default_factory=list)

def node_triage(state: AgentState) -> AgentState:
    t = state.user_input.lower()
    state.urgency = any(x in t for x in ALERTA)
    logger.info({"event": "triage", "urgency": state.urgency})
    return state

def node_retrieve(state: AgentState) -> AgentState:
    state.contexts = retrieve(settings.CHROMA_DIR, state.user_input, k=3)
    state.sources = [c["id"] for c in state.contexts]
    logger.info({"event": "retrieve", "sources": state.sources})
    return state

def build_prompt(state: AgentState) -> str:
    ctx_txt = "\n\n".join([f"[{c['id']}] {c['title']}\n{c['text']}" for c in state.contexts]) or "Sem contexto adicional."
    return f"""
Você é um assistente médico EDUCATIVO.
Regras:
- Não diagnosticar.
- Não prescrever medicamentos ou doses.
- Responder em pt-BR.
- Se houver gravidade, orientar atendimento imediato.
- Sempre citar fontes internas utilizadas no final.

Formato obrigatório:
1) Resumo do caso
2) Orientação geral
3) Sinais de alerta
4) Próximos passos
5) Fontes (IDs)

Contexto interno:
{ctx_txt}

Caso do usuário:
{state.user_input}

Responda agora:
""".strip()

def node_answer(state: AgentState) -> AgentState:
    prompt = build_prompt(state)

    if settings.USE_LOCAL_LLM:
        llm = LocalLLM(settings.LOCAL_MODEL_PATH)
        raw = llm.invoke(prompt)
    else:
        llm = make_openai_llm(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
        raw = llm.invoke(prompt).content

    ok, safe = safety_check(raw)
    if not ok:
        state.answer = safe
    else:
        # força “Fontes”
        fontes = ", ".join(state.sources) if state.sources else "N/A"
        if "fontes" not in raw.lower():
            raw += f"\n\n5) Fontes (IDs)\n- {fontes}"
        state.answer = raw

    logger.info({"event": "answer", "safe": ok, "sources": state.sources})
    return state

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("triage", node_triage)
    g.add_node("retrieve", node_retrieve)
    g.add_node("generate_answer", node_answer)

    # UM único ponto de entrada
    g.set_entry_point("triage")

    # fluxo linear correto
    g.add_edge("triage", "retrieve")
    g.add_edge("retrieve", "generate_answer")

    # FINAL explícito
    g.add_edge("generate_answer", END)

    return g.compile()

