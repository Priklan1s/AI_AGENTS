from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:14b", temperature=0)


def requirement_agent(state):

    requirements = state.get("requirements", "")
    context = state.get("context", "")

    prompt = f"""
Ты Senior QA Analyst.

Контекст:
{context}

Требования:
{requirements}

Задача:

1 найти пробелы
2 найти противоречия
3 выявить неоднозначности
4 определить риски тестирования

Формат:

### Проблемы требований
Фрагмент | Проблема | Риск
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "analysis": result
    }