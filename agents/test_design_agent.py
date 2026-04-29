import os
from langchain_ollama import OllamaLLM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR,"knowledge","test_design_rules.txt"),encoding="utf-8") as f:
    design_rules = f.read()

llm = OllamaLLM(model="deepseek-coder:6.7b")


def test_design_agent(state):

    analysis = state["analysis"]
    risks = state["risks"]

    prompt = f"""
Ты Senior QA инженер.

Используй техники тест дизайна:

{design_rules}

На основе анализа и рисков определи:

1. Какие техники тест дизайна использовать
2. Какие тестовые данные нужны
3. Какие граничные условия
4. Какие негативные сценарии

Анализ:
{analysis}

Риски:
{risks}
"""

    result = llm.invoke(prompt)

    return {
        "test_design": result
    }