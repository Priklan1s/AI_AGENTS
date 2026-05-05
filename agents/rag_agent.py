from knowledge_base.vector_store import search_context


def rag_agent(state):

    vector_store = state.get("vector_store")
    requirements = state.get("requirements", "")

    context = search_context(
        vector_store,
        requirements
    )

    return {
        **state,
        "context": context
    }