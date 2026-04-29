import streamlit as st
from graph.workflow import graph
from docx import Document
import pandas as pd
from io import BytesIO, StringIO
import csv
import pdfplumber

st.title("AI QA Assistant")

st.write("Загрузка требований и генерация тест-кейсов")


# ---------- Чтение DOCX ----------

def read_docx(file):

    doc = Document(file)

    text = "\n".join([p.text for p in doc.paragraphs])

    return text


# ---------- Чтение PDF ----------

def read_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# ---------- Создание Word отчёта ----------

def create_full_report(analysis, testcases):

    doc = Document()

    doc.add_heading("QA Анализ требований", level=1)

    # Анализ требований
    doc.add_heading("Анализ требований", level=2)
    doc.add_paragraph(analysis)

    doc.add_heading("Тест-кейсы", level=2)

    csv_buffer = StringIO(testcases)

    reader = csv.reader(csv_buffer)

    rows = list(reader)

    if len(rows) < 2:

        doc.add_paragraph("Тест-кейсы не были сгенерированы")

    else:

        header = rows[0]

        table = doc.add_table(rows=1, cols=len(header))

        for i, h in enumerate(header):
            table.rows[0].cells[i].text = h

        for r in rows[1:]:

            row_cells = table.add_row().cells

            for i in range(len(header)):

                if i < len(r):
                    row_cells[i].text = r[i]
                else:
                    row_cells[i].text = ""

    buffer = BytesIO()

    doc.save(buffer)

    return buffer.getvalue()


# ---------- Загрузка требований ----------

uploaded_file = st.file_uploader(
    "Загрузить файл требований",
    type=["txt", "docx", "pdf"]
)

requirements_text = ""

if uploaded_file:

    if uploaded_file.name.endswith(".docx"):

        requirements_text = read_docx(uploaded_file)

    elif uploaded_file.name.endswith(".pdf"):

        requirements_text = read_pdf(uploaded_file)

    else:

        requirements_text = uploaded_file.read().decode("utf-8")

else:

    requirements_text = st.text_area(
        "Или вставьте требования",
        height=250
    )


# ---------- Генерация ----------

if st.button("Сгенерировать тест-кейсы"):

    if not requirements_text.strip():

        st.warning("Добавьте требования")

        st.stop()

    with st.spinner("AI анализирует требования..."):

        result = graph.invoke({
            "requirements": requirements_text
        })

    analysis = result.get("analysis", "")
    testcases = result.get("testcases", "")

    # ---------- Анализ ----------

    st.subheader("Анализ требований")

    st.write(analysis)

    # ---------- Таблица тест-кейсов ----------

    st.subheader("Тест-кейсы")

    csv_buffer = StringIO(testcases)

    reader = csv.reader(csv_buffer)

    rows = list(reader)

    df = None

    if len(rows) < 2:

        st.write(testcases)

    else:

        header = rows[0]

        fixed_rows = []

        for r in rows[1:]:

            if len(r) < len(header):
                r += [""] * (len(header) - len(r))

            if len(r) > len(header):
                r = r[:len(header)]

            fixed_rows.append(r)

        df = pd.DataFrame(fixed_rows, columns=header)

        st.dataframe(df, use_container_width=True)

    # ---------- Word отчёт ----------

    report = create_full_report(analysis, testcases)

    st.download_button(
        label="Скачать QA отчет (Word)",
        data=report,
        file_name="qa_report.docx"
    )

    # ---------- Excel ----------

    if df is not None:

        excel_buffer = BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="Скачать тест-кейсы (Excel)",
            data=excel_buffer.getvalue(),
            file_name="testcases.xlsx"
        )