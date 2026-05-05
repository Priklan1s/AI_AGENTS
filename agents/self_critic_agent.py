from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="qwen2.5:14b",
    temperature=0
)


def self_critic_agent(state):

    testcases = state.get("testcases")
    requirements = state.get("structured_requirements")

    prompt = f"""
Ты QA Lead.

Проверь тест-кейсы.

Требования:
{requirements}

Тест-кейсы:
{testcases}

Проверь:

1 полноту покрытия
2 ошибки тест-дизайна
3 дубли
4 отсутствующие сценарии

Формат:

Проблема
Почему это ошибка
Как исправить
"""

    return {
        **state,
        "test_review": llm.invoke(prompt)
    }