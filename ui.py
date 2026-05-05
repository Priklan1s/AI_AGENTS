import streamlit as st
from graph.workflow import graph
from parsing.pdf_parser import load_pdf_text
from docx import Document
from knowledge_base.loader import load_knowledge
from knowledge_base.vector_store import create_vector_store
from langchain_ollama import OllamaLLM

st.title("AI QA Assistant")

# -----------------------------
# LLM для QA чата
# -----------------------------

chat_llm = OllamaLLM(model="qwen2.5:14b")


# -----------------------------
# состояние чата
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# -----------------------------
# загрузка требований
# -----------------------------

uploaded_file = st.file_uploader(
    "Загрузить требования",
    type=["pdf", "docx", "txt"]
)

requirements_text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):
        requirements_text = load_pdf_text(uploaded_file)

    else:
        requirements_text = uploaded_file.read().decode("utf-8")


# -----------------------------
# загрузка knowledge base
# -----------------------------

@st.cache_resource
def load_vector_store():

    knowledge_texts = load_knowledge("knowledge")

    return create_vector_store(
        knowledge_texts
    )


vector_store = load_vector_store()


# -----------------------------
# запуск AI pipeline
# -----------------------------

if st.button("Анализировать"):

    if not requirements_text:
        st.warning("Добавьте требования")
        st.stop()

    with st.spinner("AI анализирует требования..."):

        result = graph.invoke({
            "requirements": requirements_text,
            "vector_store": vector_store
        })

    if result is None:
        st.error("AI pipeline вернул пустой результат")
        st.stop()

    st.session_state.last_result = result

    # -----------------------------
    # DEBUG
    # -----------------------------

    st.subheader("DEBUG RESULT")
    st.json(result)

    # -----------------------------
    # Анализ требований
    # -----------------------------

    st.subheader("Анализ требований")

    analysis = result.get(
        "analysis",
        "Анализ требований не был сгенерирован"
    )

    st.write(analysis)

    # -----------------------------
    # Риски
    # -----------------------------

    st.subheader("Риски")

    risks = result.get(
        "risks",
        "Риски не были сгенерированы"
    )

    st.write(risks)

    # -----------------------------
    # Тест-дизайн
    # -----------------------------

    st.subheader("Тест-дизайн")

    test_design = result.get(
        "test_design",
        "Тест-дизайн отсутствует"
    )

    st.write(test_design)

    # -----------------------------
    # Тест-кейсы
    # -----------------------------

    st.subheader("Тест-кейсы")

    testcases = result.get(
        "testcases",
        "Тест-кейсы не были созданы"
    )

    st.code(testcases)


# -----------------------------
# AI QA CHAT
# -----------------------------

if st.session_state.last_result:

    st.divider()
    st.subheader("AI QA Chat — правки и уточнения")

    user_message = st.chat_input(
        "Например: добавь edge cases или перепиши тест-кейсы"
    )

    if user_message:

        result = st.session_state.last_result

        context = f"""
Ты Senior QA Engineer.

Текущий анализ требований:

{result.get("analysis","")}

Риски:

{result.get("risks","")}

Тест-дизайн:

{result.get("test_design","")}

Тест-кейсы:

{result.get("testcases","")}

Запрос пользователя:

{user_message}

Задача:

Исправь или дополни результат.

Можно:

- улучшить анализ
- добавить риски
- добавить тест-кейсы
- исправить тест-дизайн

Отвечай только на русском.
"""

        response = ""

        with st.chat_message("assistant"):

            message_placeholder = st.empty()

            for chunk in chat_llm.stream(context):

                response += chunk
                message_placeholder.markdown(response)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })


# -----------------------------
# отображение истории чата
# -----------------------------

for msg in st.session_state.chat_history:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])