# 🎓 CampusQuery-RAG

CampusQuery is an AI-powered college question-answering system built using **Retrieval-Augmented Generation (RAG)**.

The system retrieves relevant information from college documents and uses an LLM to generate grounded answers while showing the original document and page as the source.

## 🚀 Features

* 📄 PDF document ingestion
* ✂️ Intelligent document chunking
* 🧠 Sentence Transformer embeddings
* 🗄️ ChromaDB vector database
* 🔎 Semantic document retrieval
* 🤖 Groq-powered LLM generation
* 📚 Source and page references
* 💬 Streamlit chat interface
* 🔐 API keys stored securely using `.env`

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   College PDFs   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ PDF Ingestion    │
                    │     pypdf        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Text Chunking    │
                    │   LangChain      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Embeddings     │
                    │ BGE-small-en-v1.5│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    ChromaDB      │
                    └────────┬─────────┘
                             │
                    Student Question
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retriever     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Groq LLM     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Answer + Sources │
                    └──────────────────┘
```

## 📁 Project Structure

```text
CampusQuery-RAG/
│
├── app.py
├── ingest_data.py
├── pdf_ingest.py
├── retriever.py
├── llm.py
├── rag_pipeline.py
│
├── data/
│   └── college_pdfs/
│
├── chroma_db/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `data/college_pdfs/`, `chroma_db/`, `.env`, and `venv/` should not be committed to GitHub.

## 🛠️ Tech Stack

| Component             | Technology             |
| --------------------- | ---------------------- |
| Language              | Python                 |
| UI                    | Streamlit              |
| RAG Framework         | LangChain              |
| PDF Processing        | pypdf                  |
| Embeddings            | BAAI/bge-small-en-v1.5 |
| Vector Database       | ChromaDB               |
| LLM                   | Groq                   |
| Environment Variables | python-dotenv          |
| Version Control       | Git + GitHub           |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CampusQuery-RAG.git
cd CampusQuery-RAG
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install:

```bash
pip install langchain langchain-community langchain-chroma langchain-huggingface langchain-text-splitters beautifulsoup4 sentence-transformers pypdf streamlit groq python-dotenv
```

## 🔑 Configure Groq API

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit the `.env` file.

## 📚 Add College Documents

Place your PDF documents inside:

```text
data/college_pdfs/
```

For example:

```text
data/
└── college_pdfs/
    ├── academic_regulations.pdf
    ├── exam_schedule.pdf
    ├── attendance_policy.pdf
    └── student_circular.pdf
```

The project can be extended with additional official college documents whenever new information needs to be added.

## 🧠 Build the Vector Database

Run:

```bash
python pdf_ingest.py
```

This will:

1. Read the PDFs.
2. Extract text page-by-page.
3. Attach source and page metadata.
4. Split the text into chunks.
5. Generate embeddings.
6. Store the embeddings in ChromaDB.

The database will be created locally in:

```text
chroma_db/
```

## 🔎 Test Retrieval

Run:

```bash
python retriever.py
```

Example:

```text
🔎 Ask a question: When is CAT-1 scheduled?
```

The retriever will return the most relevant document chunks.

## 🤖 Test the LLM

Run:

```bash
python llm.py
```

The LLM uses retrieved context to generate grounded answers.

## 🔗 Test the Complete RAG Pipeline

Run:

```bash
python rag_pipeline.py
```

Example:

```text
🔎 Ask CampusQuery: When is CAT-1 scheduled?
```

The system will:

```text
Question
   ↓
ChromaDB Retrieval
   ↓
Relevant Context
   ↓
Groq LLM
   ↓
Answer
   ↓
Source + Page
```

## 💬 Run the Streamlit Application

Start the application:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## 🌿 Forking the Repository

If you want to contribute to CampusQuery:

### 1. Fork the repository

Open the repository on GitHub:

```text
https://github.com/YOUR_USERNAME/CampusQuery-RAG
```

Click:

```text
Fork
```

GitHub will create a copy under your own account.

### 2. Clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/CampusQuery-RAG.git
cd CampusQuery-RAG
```

### 3. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/improve-retrieval
```

### 4. Make your changes

Test the application locally before committing.

### 5. Commit your changes

```bash
git add .
git commit -m "Improve document retrieval"
```

### 6. Push your branch

```bash
git push -u origin feature/improve-retrieval
```

### 7. Create a Pull Request

Go to your GitHub fork and click:

```text
Compare & pull request
```

Describe your changes and submit the Pull Request to the original repository.

## 🔄 Keeping Your Fork Updated

Add the original repository as `upstream`:

```bash
git remote add upstream https://github.com/YOUR_USERNAME/CampusQuery-RAG.git
```

For the actual upstream project, replace the URL with the original repository URL.

Then:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

## 🔐 Files Excluded from Git

The following should remain local:

```text
.env
venv/
chroma_db/
data/college_pdfs/
__pycache__/
*.pyc
```

These files may contain secrets, generated databases, large datasets, or local environment files.

## 🧪 Current Status

### Completed

* [x] PDF ingestion
* [x] Page-level metadata
* [x] Text chunking
* [x] BGE embeddings
* [x] ChromaDB vector database
* [x] Semantic retrieval
* [x] Groq LLM integration
* [x] RAG pipeline
* [x] Streamlit interface

### Planned Improvements

* [ ] Add more official college regulations
* [ ] Add attendance/debarment documents
* [ ] Improve retrieval precision
* [ ] Add OCR for scanned PDFs
* [ ] Add better source citations
* [ ] Add evaluation dataset
* [ ] Add retrieval evaluation metrics
* [ ] Deploy the Streamlit application

## 👨‍💻 Contributors

CampusQuery-RAG is developed as a collaborative student project.

Contributions, improvements, and feedback are welcome.
