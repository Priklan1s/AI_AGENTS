from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="deepseek-coder:6.7b")

def risk_agent(state):

    analysis = state["analysis"]

    prompt = f"""
Ты QA инженер.

На основе анализа требований найди риски.

Сформируй:

1. Функциональные риски
2. Бизнес риски
3. Технические риски
4. Риски данных
5. Граничные условия

Анализ:
{analysis}
"""

    result = llm.invoke(prompt)

    return {
        "risks": result
    }