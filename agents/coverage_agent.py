from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:14b")


def coverage_agent(state):

    requirements = state.get("structured_requirements")
    testcases = state.get("testcases")

    prompt = f"""
Ты QA Architect.

Проверь покрытие требований тестами.

Требования:
{requirements}

Тест-кейсы:
{testcases}

Определи:

Covered requirements
Missing coverage
Weak tests

Формат:

Requirement
Coverage status
Comment
"""

    return {
        **state,
        "coverage": llm.invoke(prompt)
    }