from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from parsing.text_splitter import split_text


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


def create_vector_store(texts):

    chunks = []

    for text in texts:
        chunks.extend(split_text(text))

    return FAISS.from_texts(
        chunks,
        embedding=embeddings
    )


def search_context(vector_store, query, k=4):

    docs = vector_store.similarity_search(
        query[:1000],  # ограничиваем запрос
        k=k
    )

    return "\n".join([d.page_content for d in docs])