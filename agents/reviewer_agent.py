from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="deepseek-coder:6.7b")


def reviewer_agent(state):

    testcases = state["testcases"]

    prompt = f"""
Ты QA Lead.

Проверь тест кейсы.

1. Есть ли пропущенные сценарии
2. Есть ли дубли
3. Есть ли плохие тесты
4. Какие нужно добавить

Тест кейсы:
{testcases}
"""

    result = llm.invoke(prompt)

    return {
        "review": result
    }