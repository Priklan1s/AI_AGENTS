from langchain_ollama import OllamaLLM
import os
from knowledge.pdf_loader import load_pdf_text

llm = OllamaLLM(model="deepseek-coder:6.7b")


# ---------- загрузка текстовых файлов ----------

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


BASE_PATH = os.path.dirname(os.path.dirname(__file__))


QA_RULES = load_file(
    os.path.join(BASE_PATH, "knowledge", "qa_rules.txt")
)

TEST_DESIGN_RULES = load_file(
    os.path.join(BASE_PATH, "knowledge", "test_design_rules.txt")
)

TESTCASE_TEMPLATE = load_file(
    os.path.join(BASE_PATH, "knowledge", "testcase_template.txt")
)


# ---------- загрузка примеров тест-кейсов из PDF ----------

EXAMPLES = load_pdf_text(
    os.path.join(BASE_PATH, "knowledge", "testcase_examples.pdf")
)


# ---------- агент генерации тест-кейсов ----------

def testcase_agent(state):

    requirements = state.get("requirements", "")
    analysis = state.get("analysis", "")

    prompt = f"""
Ты Senior QA Engineer с большим опытом.

Твоя задача — создать качественные тест-кейсы на основе требований.

Используй правила QA:

{QA_RULES}

Используй техники тест-дизайна:

{TEST_DESIGN_RULES}

Используй следующий шаблон тест-кейса:

{TESTCASE_TEMPLATE}

Примеры хороших тест-кейсов:

{EXAMPLES}

Требования:

{requirements}

Анализ требований:

{analysis}

Составь тест-кейсы на основе уже согласованного покрытия.

Используй документ по написанию тест-кейсов test_design_rules.txt, находящийся у тебя в проекте.

Формат: Name / Objective / Preconditions / Steps / Expected Result / Traceability.

Используй нейтрально-технический стиль.

Один тест = одна логическая проверка.

Не придумывай отсутствующие элементы UI, сообщения и условия доступа.

Учитывай роли, права, состояния, ошибки, empty states и edge cases.

Финальный результат подготовь в структуре, пригодной для последующего экспорта / формирования CSV для импорта в Zephyr.
Если возможно, сразу собери тест-кейсы как CSV-набор с отдельными колонками для всех обязательных полей.
Строго соблюдай CSV формат.

Колонки:

ID,Name,Objective,Preconditions,Steps,Expected Result,Traceability

Каждый тест-кейс — новая строка.

Steps разделяй символом |.
"""

    result = llm.invoke(prompt)

    return {"testcases": result}