from langchain_ollama import OllamaLLM
from parsing.text_splitter import split_text

llm = OllamaLLM(
    model="qwen2.5:14b",
    temperature=0
)

def requirement_structurer(state):

    requirements = state.get("requirements", "")

    chunks = split_text(requirements)

    structured = ""

    for chunk in chunks:

        prompt = f"""
Ты системный аналитик.

Структурируй требования.

Текст:
{chunk}

Выдели:

- функции системы
- роли пользователей
- действия
- ожидаемые результаты

Формат:

Feature:
Actors:
Steps:
Result:

Пиши только на русском.
"""

        structured += llm.invoke(prompt)

    return {
        **state,
        "structured_requirements": structured
    }