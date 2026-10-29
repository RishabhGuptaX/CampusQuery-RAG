
import hashlib
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PDF_FOLDER = Path("data/college_pdfs")
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "campusquery"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


def read_pdf_pages(pdf_path: Path) -> list[Document]:
    """Extract usable text while preserving filename and page number."""
    documents = []

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = (page.extract_text() or "").strip()
        except Exception as exc:
            print(f"   Warning: page {page_number}: {exc}")
            continue

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


def stable_chunk_id(source: str, index: int, text: str) -> str:
    """Produce a deterministic ID for each source chunk."""
    payload = f"{source}|{index}|{text}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    print("=" * 60)
    print("CAMPUSQUERY - INCREMENTAL PDF INDEXING")
    print("=" * 60)

    if not PDF_FOLDER.exists():
        print(f"PDF folder not found: {PDF_FOLDER}")
        return

    pdf_files = sorted(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDFs found.")
        return

    print(f"PDF files discovered: {len(pdf_files)}")

    print("\nLoading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Open the existing collection; do not delete or recreate it.
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    stored = vectorstore.get(include=["metadatas"])
    existing_sources = {
        str(metadata["source"]).casefold()
        for metadata in (stored.get("metadatas") or [])
        if metadata and metadata.get("source")
    }

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    indexed_files = 0
    skipped_files = 0
    failed_files = 0
    total_chunks = 0

    for pdf_path in pdf_files:
        source = pdf_path.name

        if source.casefold() in existing_sources:
            print(f"\nAlready indexed; skipping: {source}")
            skipped_files += 1
            continue

        print(f"\nProcessing: {source}")

        try:
            pages = read_pdf_pages(pdf_path)

            if not pages:
                print(
                    "   No usable text extracted. "
                    "This PDF may be scanned and need OCR."
                )
                continue

            chunks = splitter.split_documents(pages)

            if not chunks:
                print("   No chunks generated; skipping.")
                continue

            ids = [
                stable_chunk_id(source, index, chunk.page_content)
                for index, chunk in enumerate(chunks)
            ]

            # Explicit deterministic IDs avoid duplicates when the same
            # chunks are submitted again to this collection.
            vectorstore.add_documents(
                documents=chunks,
                ids=ids,
            )

            existing_sources.add(source.casefold())
            indexed_files += 1
            total_chunks += len(chunks)

            print(
                f"   Pages extracted: {len(pages)} | "
                f"Chunks indexed: {len(chunks)}"
            )

        except Exception as exc:
            failed_files += 1
            print(f"   ERROR: {exc}")

    print("\n" + "=" * 60)
    print("INDEXING SUMMARY")
    print("=" * 60)
    print(f"New files indexed: {indexed_files}")
    print(f"Already indexed files skipped: {skipped_files}")
    print(f"Files with errors: {failed_files}")
    print(f"New chunks submitted: {total_chunks}")

    try:
        final_count = vectorstore._collection.count()
        print(f"Total chunks in ChromaDB: {final_count}")
    except Exception as exc:
        print(f"Could not read collection count: {exc}")

    print("\nIndexing finished.")


if __name__ == "__main__":
    main()
