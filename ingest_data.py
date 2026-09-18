import re
import os
from bs4 import BeautifulSoup

# --- LANGCHAIN IMPORTS ---
# 1. For Scraping
from langchain_community.document_loaders import RecursiveUrlLoader
# 2. For Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 3. For Embeddings 
from langchain_huggingface import HuggingFaceEmbeddings
# 4. For Vector Database
from langchain_chroma import Chroma

# ==========================================
# STEP 1: DEFINE THE HTML CLEANER
# ==========================================
def bs4_extractor(html: str) -> str:
    """Extracts only the meaningful article text from the raw HTML."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Strip out headers, footers, and navigation menus (the 'noise')
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        element.decompose()
        
    # Get the text and fix the spacing
    text = soup.get_text(separator='\n', strip=True)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def build_rag_database():
    # ==========================================
    # STEP 2: SCRAPE THE WEBSITE
    # ==========================================
    print("1. Starting LangChain web crawler...")
    
    # prevent_outside=True stops it from leaving vitap.ac.in
    # max_depth=2 keeps the crawl manageable. (Increase to 4+ for the whole site later)
    loader = RecursiveUrlLoader(
        url="https://vitap.ac.in/",
        extractor=bs4_extractor,
        prevent_outside=True,
        max_depth=2 
    )
    
    # Load all pages into LangChain 'Document' objects
    docs = loader.load()
    print(f"   -> Successfully loaded {len(docs)} pages.")

    if not docs:
        print("No documents found. Exiting.")
        return

    # ==========================================
    # STEP 3: CHUNK THE TEXT
    # ==========================================
    print("\n2. Chunking the documents...")
    
    # 1000 characters per chunk, with 200 characters of overlap to maintain context
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    # Split the large page documents into smaller chunks
    chunks = text_splitter.split_documents(docs)
    print(f"   -> Split into {len(chunks)} chunks.")

    # ==========================================
    # STEP 4: EMBED AND STORE IN CHROMADB
    # ==========================================
    print("\n3. Downloading/Loading embedding model...")
    # BAAI/bge-small-en-v1.5 is widely considered one of the best free, lightweight models for RAG
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print("\n4. Generating embeddings and building Vector DB...")
    # The folder where your database will be saved permanently
    persist_directory = "./chroma_db"
    
    # Create the database and save it to the disk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"\n✅ SUCCESS! Vector database has been saved to the '{persist_directory}' folder.")
    print("Your RAG knowledge base is ready to be queried.")

if __name__ == "__main__":
    build_rag_database()
