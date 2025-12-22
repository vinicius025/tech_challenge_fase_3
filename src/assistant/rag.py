import json
from pathlib import Path
import chromadb

def build_vector_store(chroma_dir: str, protocols_path: str = "data/raw/protocols.json"):
    client = chromadb.PersistentClient(path=chroma_dir)
    col = client.get_or_create_collection("protocols")

    protocols = json.loads(Path(protocols_path).read_text(encoding="utf-8"))
    docs, ids, metas = [], [], []

    for p in protocols:
        ids.append(p["id"])
        docs.append(p["content"])
        metas.append({"title": p["title"], "source_id": p["id"]})

    col.upsert(ids=ids, documents=docs, metadatas=metas)
    return True

def retrieve(chroma_dir: str, query: str, k: int = 3):
    client = chromadb.PersistentClient(path=chroma_dir)
    col = client.get_or_create_collection("protocols")
    res = col.query(query_texts=[query], n_results=k)
    hits = []
    for doc, meta, _id in zip(res["documents"][0], res["metadatas"][0], res["ids"][0]):
        hits.append({"id": _id, "title": meta.get("title"), "text": doc})
    return hits
