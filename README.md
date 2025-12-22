# Assistente Médico Virtual Educativo – Tech Challenge (Fase 3)

Este projeto foi desenvolvido como parte do Tech Challenge – Fase 3, com o objetivo de construir um Assistente Médico Virtual Educativo, utilizando Modelos de Linguagem de Grande Porte (LLMs), fine-tuning com LoRA, RAG (Retrieval-Augmented Generation) e orquestração de fluxos de decisão com LangGraph.

O sistema foi projetado para demonstrar uma aplicação de IA segura, explicável, auditável e eticamente responsável, voltada exclusivamente para fins educacionais, conforme as diretrizes do desafio.

---

## Objetivo

Desenvolver um assistente virtual capaz de oferecer orientações clínicas educativas, sem realizar diagnósticos médicos ou prescrições, garantindo:
- Triagem inicial de urgência baseada em regras
- Respostas em linguagem natural controlada
- Recuperação de contexto clínico interno via RAG
- Fluxo de decisão organizado e auditável
- Registro completo das interações (logging)
- Conformidade com boas práticas de segurança em IA

---

## Escopo e Limitações

Este sistema:
- Não substitui avaliação médica profissional
- Não realiza diagnósticos definitivos
- Não prescreve medicamentos ou dosagens
- Atua exclusivamente como ferramenta educacional e demonstrativa

---

## Dataset

### Origem dos Dados
- Dataset inteiramente sintético, criado para fins educacionais
Inspirado em:
- Protocolos clínicos genéricos (ex.: hipertensão, dor torácica)
- Perguntas frequentes em contextos de saúde
- Cenários de triagem e orientação clínica

---

## Anonimização

Antes do treinamento, todos os textos passam por um módulo de anonimização que remove:
- CPF
- CNPJ
- Telefones
- E-mails

---

## Estrutura do Projeto

```bash
TECH_CHALLENGE_FASE_3/
│
├── data/
│   ├── raw/                 # Dados brutos sintéticos
│   ├── processed/           # Dados pré-processados e anonimizados
│   └── synthetic/           # Protocolos clínicos e dados artificiais
│
├── models/
│   └── finetuned/           # Modelo LLM fine-tuned com LoRA
│
├── logs/
│   └── app.log              # Logs de auditoria e rastreabilidade
│
├── reports/
│   └── diagrams/            # Diagramas do fluxo (LangChain / LangGraph)
│
├── src/
│   └── assistant/
│       ├── app_cli.py       # Interface CLI do assistente
│       ├── graph.py         # Fluxo automatizado com LangGraph
│       ├── llm_openai.py    # Integração com OpenAI (fallback)
│       ├── llm_local.py     # Integração com modelo fine-tuned local
│       ├── rag.py           # Recuperação de contexto (RAG)
│       ├── security.py      # Guardrails e validações de segurança
│       ├── logging_conf.py  # Configuração de logging
│       └── pii.py           # Anonimização de dados sensíveis
│
├── training/
│   ├── make_synth_dataset.py  # Geração de dataset sintético
│   ├── preprocess.py          # Pré-processamento e anonimização
│   ├── finetune_lora.py       # Fine-tuning do modelo com LoRA
│   └── evaluate_finetune.py   # Avaliação qualitativa do modelo
│
├── scripts/
│   ├── setup.ps1             # Script de setup (Windows)
│   └── setup.sh              # Script de setup (Linux/Mac)
│
├── requirements.txt          # Dependências do projeto
├── Dockerfile                # Containerização do projeto
├── docker-compose.yml        # Execução local via Docker
├── .env.example              # Exemplo de variáveis de ambiente
└── README.md                 # Documentação do projeto
```


---

## Tecnologias Utilizadas

| Categoria                     | Tecnologias                           |
| ----------------------------- | ------------------------------------- |
| Linguagem                     | Python 3.11                           |
| Modelo de Linguagem (LLM)     | TinyLlama-1.1B-Chat                   |
| Fine-Tuning                   | LoRA (PEFT)                           |
| RAG (Recuperação de Contexto) | LangChain, Chroma                     |
| Orquestração de Fluxos        | LangGraph                             |
| Embeddings                    | Sentence Transformers                 |
| Integração LLM (Fallback)     | OpenAI API                            |
| Logging e Auditoria           | Loguru                                |
| Infraestrutura                | Execução local (CPU)                  |
| Containerização               | Docker, Docker Compose                |
| Outras                        | Transformers, Datasets, Torch, dotenv |

---

## Fluxo do Projeto — Fase 3

1. Geração de Dados Sintéticos  
   - Criação de cenários clínicos educacionais.  
   - Organização no formato instrução–resposta.

2. Pré-processamento e Anonimização  
   - Limpeza dos textos.  
   - Remoção de dados sensíveis.  
   - Preparação dos dados para fine-tuning.

3. Fine-Tuning do Modelo (LoRA) 
   - Modelo base: TinyLlama-1.1B-Chat.
   - Técnica: LoRA (Low-Rank Adaptation)
   - Execução local em CPU
   - Avaliação qualitativa do comportamento do modelo

4. RAG – Recuperação de Contexto  
   - Indexação de protocolos clínicos artificiais.  
   - Busca vetorial para contextualização das respostas.
   - Exibição explícita das fontes utilizadas

5. Orquestração com LangGraph
   - Triagem de urgência
   - Recuperação de contexto clínico
   - Geração da resposta
   - Geração da resposta
   - Validação de segurança
   - Logging e auditoria

---

## Resultados do Fine-Tuning

Durante o treinamento com LoRA, o modelo apresentou:
- Convergência estável do treinamento
- Redução consistente da função de perda (loss)
- Alta acurácia média por token
- Comportamento cauteloso e educativo nas respostas

A avaliação qualitativa demonstrou que o modelo:

- Evita diagnósticos fechados
- Solicita informações adicionais quando necessário
- Mantém linguagem adequada ao contexto clínico educacional

---

## Execução do Projeto

### Criar ambiente virtual
```bash
  python -m venv .venv
  source .venv/bin/activate (Linux/Mac)
  .venv\Scripts\Activate.ps1 (Windows)
```

### Instalar dependências
```bash
  pip install -r requirements.txt
```
### Executar o assistente
```bash
  python -m src.assistant.app_cli
```
---

## Exemplos de Uso

### Caso sem urgência
  - Paciente com pressão arterial de 150x95 em medições repetidas, sem outros sintomas.

### Caso com urgência
  - Paciente com dor no peito e falta de ar há 30 minutos.

O sistema realiza a triagem, recupera protocolos clínicos relevantes, gera uma resposta educativa e registra toda a interação em log.

---

## Logging e Auditoria

Todos os eventos são registrados no arquivo:
  - logs/app.log

Incluindo:
  - Entrada do usuário
  - Classificação de urgência
  - Protocolos recuperados via RAG
  - Resposta final
  - Aplicação de regras de segurança

Esse mecanismo garante rastreabilidade completa do comportamento do assistente.

---

## Considerações Finais

Este projeto demonstra a aplicação integrada de:
  - LLMs fine-tuned com LoRA
  - Recuperação de contexto com RAG
  - Orquestração de decisões com LangGraph
  - Boas práticas de IA responsável e segura

O foco foi a construção de um sistema educacional, explicável e auditável, alinhado às exigências do Tech Challenge – Fase 3.

---

## Aviso

Este projeto possui finalidade exclusivamente acadêmica
e não deve ser utilizado como ferramenta clínica real.

---

**Link do Vídeo de Demonstração**

- Vídeo de demonstração part 3: