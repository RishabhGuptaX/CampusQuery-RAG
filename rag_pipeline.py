from retriever import search_documents
from llm import generate_answer


# ============================================================
# CAMPUSQUERY — RAG PIPELINE
# ============================================================


def build_context(results):
    """
    Convert retrieved documents into context for the LLM.
    """

    context_parts = []

    for i, document in enumerate(results, start=1):

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        context_parts.append(
            f"""
SOURCE {i}
Document: {source}
Page: {page}

Content:
{document.page_content}
"""
        )

    return "\n".join(context_parts)


def ask_campusquery(question, k=5):
    """
    Complete RAG pipeline:

    Question
        ↓
    Retrieval
        ↓
    Context construction
        ↓
    LLM
        ↓
    Answer + sources
    """

    # --------------------------------------------------------
    # 1. Retrieve relevant documents
    # --------------------------------------------------------

    results = search_documents(
        question,
        k=k
    )

    if not results:
        return {
            "answer": (
                "I couldn't find this information in "
                "the available college documents."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # 2. Build context
    # --------------------------------------------------------

    context = build_context(results)

    # --------------------------------------------------------
    # 3. Generate answer
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        context
    )

    # --------------------------------------------------------
    # 4. Extract sources
    # --------------------------------------------------------

    sources = []

    seen = set()

    for document in results:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        source_key = (source, page)

        # Avoid duplicate sources
        if source_key not in seen:

            sources.append({
                "source": source,
                "page": page
            })

            seen.add(source_key)

    return {
        "answer": answer,
        "sources": sources
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("       CAMPUSQUERY — RAG PIPELINE")
    print("=" * 60)

    question = input("\n🔎 Ask CampusQuery: ").strip()

    if not question:

        print("❌ Please enter a question.")

    else:

        print("\n🔍 Searching college documents...")

        result = ask_campusquery(question)

        print("\n" + "=" * 60)
        print("🤖 ANSWER")
        print("=" * 60)

        print(result["answer"])

        print("\n" + "=" * 60)
        print("📚 SOURCES")
        print("=" * 60)

        if result["sources"]:

            for i, source in enumerate(
                result["sources"],
                start=1
            ):

                print(
                    f"{i}. {source['source']} "
                    f"(Page {source['page']})"
                )

        else:

            print("No sources found.")

        print("\n" + "=" * 60)