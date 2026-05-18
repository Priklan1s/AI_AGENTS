from langchain_ollama import OllamaLLM
import os

llm = OllamaLLM(
    model="qwen2.5:14b",
    temperature=0
)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


BASE_PATH = os.path.dirname(os.path.dirname(__file__))

QA_RULES = load_file(os.path.join(BASE_PATH, "knowledge", "qa_rules.txt"))
TEST_DESIGN_RULES = load_file(os.path.join(BASE_PATH, "knowledge", "test_design_rules.txt"))
TESTCASE_TEMPLATE = load_file(os.path.join(BASE_PATH, "knowledge", "testcase_template.txt"))


def testcase_agent(state):

    requirements = state.get("requirements", "")
    analysis = state.get("analysis", "")

    prompt = f"""
Ты Senior QA Engineer.

Отвечай ТОЛЬКО на русском языке.

Используй правила QA:

{QA_RULES}

Используй правила тест-дизайна:

{TEST_DESIGN_RULES}

Шаблон тест-кейсов:

{TESTCASE_TEMPLATE}

---

ТРЕБОВАНИЯ

{requirements}

---

АНАЛИЗ ТРЕБОВАНИЙ

{analysis}

---

ЗАДАЧА

Составь тест-кейсы.

Правила:

• один тест = одна проверка  
• покрыть позитивные сценарии  
• покрыть негативные сценарии  
• покрыть edge cases  
• учитывать роли и права  

Не придумывай элементы интерфейса.

---

ФОРМАТ CSV

ID,Name,Objective,Preconditions,Steps,Expected Result,Traceability

Steps разделяй символом |

Сделай полное тестовое покрытие тест-кейсами.
"""

    result = ""

    for chunk in llm.stream(prompt):
        result += chunk

    return {
        **state,
        "testcases": result
    }