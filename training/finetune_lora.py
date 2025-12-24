from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl.trainer import SFTTrainer
from peft import LoraConfig
from pathlib import Path

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
OUT_DIR = "models/finetuned"


def formatting(example):
    return [f"""### Instrução
{example['input']}

### Resposta
{example['output']}
"""]




def main():
    # 1. Load dataset
    data_files = {
        "train": "data/processed/train.jsonl",
        "validation": "data/processed/val.jsonl",
    }
    ds = load_dataset("json", data_files=data_files)

    train_dataset = ds["train"]
    eval_dataset = ds["validation"]

    # 2. Tokenizer
    tok = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    # 3. Model
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

    # 4. LoRA config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # 5. Training arguments
    args = TrainingArguments(
        output_dir=OUT_DIR,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=2,
        learning_rate=2e-4,
        logging_steps=20,
        eval_steps=50,
        eval_strategy="steps",
        save_steps=50,
        save_total_limit=2,
        fp16=False,  # ajuste se tiver GPU
        report_to="none",
    )

    # 6. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=lora_config,
        args=args,
        formatting_func=formatting,
    )


    # 7. Train
    trainer.train()

    # 8. Save model
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    trainer.model.save_pretrained(OUT_DIR)
    tok.save_pretrained(OUT_DIR)

    print("OK: fine-tuning (LoRA) concluído.")


if __name__ == "__main__":
    main()