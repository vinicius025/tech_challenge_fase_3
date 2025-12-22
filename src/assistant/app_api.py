from fastapi import FastAPI
from pydantic import BaseModel
from .config import settings
from .rag import build_vector_store
from .graph import build_graph, AgentState

app = FastAPI(title="Assistente Médico Virtual - Fase 3")

class Query(BaseModel):
    caso: str

build_vector_store(settings.CHROMA_DIR)
graph = build_graph()

@app.post("/ask")
def ask(q: Query):
    out = graph.invoke(AgentState(user_input=q.caso))
    return {"answer": out.answer}
