import json
from pathlib import Path
from src.assistant.pii import anonymize_text

def preprocess_jsonl(inp: str, out: str):
    inp_p = Path(inp)
    out_p = Path(out)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    with inp_p.open("r", encoding="utf-8") as fin, out_p.open("w", encoding="utf-8") as fout:
        for line in fin:
            row = json.loads(line)
            row["input"] = anonymize_text(row["input"])
            row["output"] = anonymize_text(row["output"])
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    preprocess_jsonl("data/raw/train.jsonl", "data/processed/train.jsonl")
    preprocess_jsonl("data/raw/val.jsonl", "data/processed/val.jsonl")
    print("OK: preprocess + anonimização concluídos.")
