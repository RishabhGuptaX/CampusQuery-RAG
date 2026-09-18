# CampusQuery

CampusQuery is a Retrieval-Augmented Generation (RAG) system designed to answer questions based on the college website data (vitap.ac.in).

## What We Have Done So Far

1. **Environment Setup**: 
   Set up a Python virtual environment and installed the necessary LangChain ecosystem dependencies (`langchain`, `langchain-community`, `langchain-chroma`, `sentence-transformers`, `beautifulsoup4`).

2. **Data Ingestion Script (`ingest_data.py`)**: 
   Built the initial pipeline to ingest data into our RAG system. The script performs the following steps:
   - **Web Scraping**: Crawls the college website (`vitap.ac.in`) to extract meaningful text, automatically filtering out noise like headers, footers, and navigation menus using `BeautifulSoup`.
   - **Data Chunking**: Splits the extracted documents into smaller chunks (1000 characters each, with 200 characters of overlap) using `RecursiveCharacterTextSplitter` so the LLM can process them effectively.
   - **Embeddings & Vector Database**: Uses the lightweight HuggingFace model `BAAI/bge-small-en-v1.5` to generate vector embeddings for the text chunks, and stores them in a local Chroma vector database (saved in the `chroma_db` directory).

3. **Execution**: 
   The script has been successfully executed, and the vector database is fully populated and ready for the retrieval and Q&A implementation.

## Next Steps
- Develop the retrieval script to search the `chroma_db` for relevant chunks based on user queries.
- Integrate a Large Language Model (LLM) to generate answers using the retrieved context.

## Running Locally
*(Note: The `chroma_db` and `venv` directories are git-ignored to keep the repository clean.)*

To regenerate the vector database on your local machine:
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install langchain langchain-community langchain-chroma langchain-huggingface langchain-text-splitters beautifulsoup4 sentence-transformers`
4. Run the script: `python ingest_data.py`
