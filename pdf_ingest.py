import hashlib
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# CONFIGURATION
# ============================================================

PDF_FOLDER = Path("data/college_pdfs")
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "campusquery"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ============================================================
# STEP 1: EXTRACT TEXT FROM PDF FILES
# ============================================================

def read_pdf_pages(pdf_path: Path) -> list[Document]:
    """
    Extract text from a PDF page by page.

    Metadata preserves the filename and original page number,
    which CampusQuery uses to display source citations.
    """
    documents = []

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = (page.extract_text() or "").strip()
        except Exception as exc:
            print(f"   Warning: page {page_number}: {exc}")
            continue

        # Ignore pages containing almost no extractable text.
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

    return documents


# ============================================================
# STEP 2: CREATE STABLE CHUNK IDS
# ============================================================

def stable_chunk_id(source: str, index: int, text: str) -> str:
    """
    Generate a deterministic ID for a chunk.

    Identical source names, chunk positions, and content produce
    the same ID.
    """
    payload = f"{source}|{index}|{text}"

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


# ============================================================
# STEP 3: INITIALIZE THE VECTOR DATABASE
# ============================================================

def open_vector_database(embeddings):
    """
    Open the existing ChromaDB collection.

    If the collection does not exist, ChromaDB creates it.
    Existing collections are not deleted or reset.
    """
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


# ============================================================
# STEP 4: INDEX NEW PDF DOCUMENTS
# ============================================================

def index_pdfs(vectorstore, pdf_files: list[Path]) -> dict:
    """
    Index PDFs that are not already represented by their source
    filename in the existing ChromaDB collection.
    """
    stored_data = vectorstore.get(include=["metadatas"])

    existing_sources = {
        str(metadata["source"]).casefold()
        for metadata in (stored_data.get("metadatas") or [])
        if metadata and metadata.get("source")
    }

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    stats = {
        "indexed": 0,
        "skipped": 0,
        "failed": 0,
        "empty": 0,
        "pages": 0,
        "chunks": 0,
    }

    for pdf_path in pdf_files:
        source = pdf_path.name

        # Skip files already represented in the database.
        if source.casefold() in existing_sources:
            print(f"\nAlready indexed; skipping: {source}")
            stats["skipped"] += 1
            continue

        print(f"\nProcessing: {source}")

        try:
            pages = read_pdf_pages(pdf_path)

            if not pages:
                print(
                    "   No usable text extracted. "
                    "This file may be scanned or image-based."
                )
                stats["empty"] += 1
                continue

            chunks = splitter.split_documents(pages)

            if not chunks:
                print("   No chunks generated.")
                stats["empty"] += 1
                continue

            chunk_ids = [
                stable_chunk_id(
                    source,
                    index,
                    chunk.page_content,
                )
                for index, chunk in enumerate(chunks)
            ]

            # Add new chunks to the existing collection.
            # Explicit IDs help prevent duplicate IDs.
            vectorstore.add_documents(
                documents=chunks,
                ids=chunk_ids,
            )

            existing_sources.add(source.casefold())

            stats["indexed"] += 1
            stats["pages"] += len(pages)
            stats["chunks"] += len(chunks)

            print(f"   Pages extracted: {len(pages)}")
            print(f"   Chunks indexed: {len(chunks)}")

        except Exception as exc:
            stats["failed"] += 1
            print(f"   ERROR processing {source}: {exc}")

    return stats


# ============================================================
# STEP 5: VERIFY THE VECTOR DATABASE
# ============================================================

def test_vector_database(vectorstore):
    """Run a sample retrieval query against the collection."""
    print("\nTesting vector database retrieval...")

    test_query = "CAT 1 examination schedule"

    try:
        results = vectorstore.similarity_search(
            test_query,
            k=3,
        )

        print(f"\nTest query: {test_query}")

        if not results:
            print("No results returned.")
            return

        for index, result in enumerate(results, start=1):
            print(f"\n--- Result {index} ---")
            print(f"Source: {result.metadata.get('source', 'Unknown')}")
            print(f"Page: {result.metadata.get('page', 'Unknown')}")
            print(f"Text: {result.page_content[:350]}")

    except Exception as exc:
        print(f"Retrieval test failed: {exc}")


# ============================================================
# STEP 6: MAIN
# ============================================================

def main():
    print("=" * 65)
    print("       CAMPUSQUERY - INCREMENTAL PDF INDEXING")
    print("=" * 65)

    # Validate the input directory.
    if not PDF_FOLDER.exists():
        print(f"\nERROR: PDF folder not found: {PDF_FOLDER}")
        print("Run this script from the CampusQuery project root.")
        return

    pdf_files = sorted(
        path
        for path in PDF_FOLDER.glob("*.pdf")
        if path.is_file()
    )

    if not pdf_files:
        print(f"\nNo PDF files found in {PDF_FOLDER}")
        return

    print(f"\nPDF directory: {PDF_FOLDER.resolve()}")
    print(f"PDF files discovered: {len(pdf_files)}")

    # Initialize the embedding model.
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    except Exception as exc:
        print(f"Could not load embedding model: {exc}")
        return

    print("Embedding model loaded.")

    # Open the existing database.
    try:
        vectorstore = open_vector_database(embeddings)
    except Exception as exc:
        print(f"Could not open ChromaDB: {exc}")
        return

    try:
        chunks_before = vectorstore._collection.count()
    except Exception:
        chunks_before = None

    print(f"Database directory: {Path(CHROMA_DIR).resolve()}")

    if chunks_before is not None:
        print(f"Chunks before indexing: {chunks_before}")

    # Index new files.
    stats = index_pdfs(vectorstore, pdf_files)

    # Report final collection count.
    try:
        chunks_after = vectorstore._collection.count()
    except Exception:
        chunks_after = None

    print("\n" + "=" * 65)
    print("                 INDEXING SUMMARY")
    print("=" * 65)

    print(f"PDF files discovered: {len(pdf_files)}")
    print(f"New PDFs indexed: {stats['indexed']}")
    print(f"Already indexed PDFs skipped: {stats['skipped']}")
    print(f"PDFs with no usable text: {stats['empty']}")
    print(f"PDFs with processing errors: {stats['failed']}")
    print(f"Pages extracted from new PDFs: {stats['pages']}")
    print(f"New chunks submitted: {stats['chunks']}")

    if chunks_after is not None:
        print(f"Total chunks now in ChromaDB: {chunks_after}")

    print(f"Database: {Path(CHROMA_DIR).resolve()}")

    # Test retrieval if indexing completed without file errors.
    if chunks_after is not None and chunks_after > 0:
        test_vector_database(vectorstore)

    print("\nIndexing process finished.")
    print("=" * 65)


if __name__ == "__main__":
    main()