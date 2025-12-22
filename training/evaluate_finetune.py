from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_DIR = "models/finetuned"

def generate(prompt: str):
    tok = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
    inputs = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=220, do_sample=True, temperature=0.3)
    return tok.decode(out[0], skip_special_tokens=True)

if __name__ == "__main__":
    p = "### Instrução\nCASO: Paciente com dor no peito e falta de ar há 30 minutos.\n\n### Resposta\n"
    print(generate(p))
