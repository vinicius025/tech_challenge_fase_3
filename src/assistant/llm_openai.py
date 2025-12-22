from langchain_openai import ChatOpenAI

def make_openai_llm(api_key: str, model: str):
    return ChatOpenAI(model=model, temperature=0.3, api_key=api_key)
