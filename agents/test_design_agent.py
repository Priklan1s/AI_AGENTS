from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:14b")

def test_design_agent(state):

    requirements = state.get("structured_requirements", "")
    analysis = state.get("analysis", "")

    prompt = f"""
Ты Senior QA Engineer.

На основе требований и анализа сформируй test coverage.

Требования:
{requirements}

Анализ:
{analysis}

Определи:

positive scenarios
negative scenarios
edge cases
roles
boundary tests
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "test_design": result
    }