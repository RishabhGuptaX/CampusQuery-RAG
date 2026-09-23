import os
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PDF_FOLDER = Path("data/college_pdfs")
CHROMA_DIR = "./chroma_db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# --------------------------------------------------
# Step 1: Extract text from PDFs
# --------------------------------------------------

def load_pdfs():

    documents = []

    if not PDF_FOLDER.exists():
        print(f"❌ PDF folder not found: {PDF_FOLDER}")
        return documents

    pdf_files = sorted(PDF_FOLDER.glob("*.pdf"))

    print(f"📚 Found {len(pdf_files)} PDF files.\n")

    for pdf_path in pdf_files:

        print(f"📄 Processing: {pdf_path.name}")

        try:

            reader = PdfReader(str(pdf_path))

            extracted_pages = 0
            total_chars = 0

            for page_number, page in enumerate(reader.pages, start=1):

                text = page.extract_text()

                if not text:
                    text = ""

                text = text.strip()

                # Ignore pages with almost no extractable text
                if len(text) < 50:
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": pdf_path.name,
                            "page": page_number,
                        },
                    )
                )

                extracted_pages += 1
                total_chars += len(text)

            if extracted_pages == 0:

                print(
                    "   ⚠️ No usable text extracted "
                    "(possible scanned PDF)"
                )

            else:

                print(
                    f"   ✅ {extracted_pages} pages extracted "
                    f"({total_chars:,} characters)"
                )

        except Exception as e:

            print(f"   ❌ Error: {e}")

    return documents


# --------------------------------------------------
# Step 2: Split documents into chunks
# --------------------------------------------------

def create_chunks(documents):

    print("\n✂️ Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    print(f"✅ Created {len(chunks):,} chunks.")

    return chunks


# --------------------------------------------------
# Step 3: Create embeddings
# --------------------------------------------------

def create_embeddings():

    print("\n🧠 Loading embedding model...")
    print(f"   Model: {EMBEDDING_MODEL}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("✅ Embedding model loaded.")

    return embeddings


# --------------------------------------------------
# Step 4: Store chunks in ChromaDB
# --------------------------------------------------

def create_vector_database(chunks, embeddings):

    print("\n🗄️ Creating ChromaDB...")

    # Create directory if it doesn't exist
    os.makedirs(CHROMA_DIR, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="campusquery"
    )

    print("✅ ChromaDB created successfully.")

    return vectorstore


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("       CAMPUSQUERY — PDF VECTOR DATABASE")
    print("=" * 60)

    # 1. Extract
    documents = load_pdfs()

    if not documents:

        print("\n❌ No documents extracted.")
        return

    print(f"\n📑 Total extracted pages: {len(documents):,}")

    # 2. Chunk
    chunks = create_chunks(documents)

    if not chunks:

        print("\n❌ No chunks created.")
        return

    # 3. Embeddings
    embeddings = create_embeddings()

    # 4. Chroma
    vectorstore = create_vector_database(
        chunks,
        embeddings
    )

    # --------------------------------------------------
    # Test the database
    # --------------------------------------------------

    print("\n🔎 Testing vector database...")

    test_query = "CAT 1 examination schedule"

    results = vectorstore.similarity_search(
        test_query,
        k=3
    )

    print(f"\nQuery: {test_query}")
    print("\nTop results:")

    for i, result in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")

        print(
            f"Source: {result.metadata.get('source')}"
        )

        print(
            f"Page: {result.metadata.get('page')}"
        )

        print(
            result.page_content[:500]
        )

    print("\n" + "=" * 60)
    print("🎉 CAMPUSQUERY VECTOR DATABASE READY")
    print("=" * 60)

    print(f"\n📁 Database location: {CHROMA_DIR}")
    print(f"📦 Total chunks: {len(chunks):,}")


if __name__ == "__main__":
    main()