from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="qwen2.5:14b")

def risk_agent(state):

    requirements = state.get("structured_requirements", "")

    prompt = f"""
Ты QA Risk Analyst.

Определи тестовые риски.

{requirements}

Формат:

Risk
Probability
Impact
Mitigation
"""

    result = llm.invoke(prompt)

    return {
        **state,
        "risks": result
    }