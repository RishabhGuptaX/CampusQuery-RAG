from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "campusquery"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# --------------------------------------------------
# Load vector database
# --------------------------------------------------

def load_vectorstore():

    print("🧠 Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("🗄️ Loading ChromaDB...")

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    print("✅ ChromaDB loaded.")

    return vectorstore


# --------------------------------------------------
# Search documents
# --------------------------------------------------

def search_documents(query, k=5):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results


# --------------------------------------------------
# Display results
# --------------------------------------------------

def main():

    print("=" * 60)
    print("       CAMPUSQUERY — RETRIEVER")
    print("=" * 60)

    query = input("\n🔎 Ask a question: ").strip()

    if not query:
        print("❌ Please enter a question.")
        return

    results = search_documents(query, k=5)

    print("\n" + "=" * 60)
    print(f"🔍 RESULTS FOR: {query}")
    print("=" * 60)

    if not results:
        print("\n❌ No relevant documents found.")
        return

    for i, result in enumerate(results, start=1):

        source = result.metadata.get(
            "source",
            "Unknown source"
        )

        page = result.metadata.get(
            "page",
            "Unknown page"
        )

        print(f"\n--- Result {i} ---")
        print(f"📄 Source: {source}")
        print(f"📑 Page: {page}")
        print("\n" + result.page_content[:1000])


if __name__ == "__main__":
    main()