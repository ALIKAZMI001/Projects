"""RAG over a PDF: chunk → embed → store in Qdrant → retrieve → answer.

Stack: LangChain + sentence-transformers embeddings + Qdrant (local, on-disk)
+ any OpenRouter chat model.

Setup:
    pip install -r requirements.txt
    set OPENROUTER_API_KEY=sk-or-...        (PowerShell: $env:OPENROUTER_API_KEY="...")

Run:  python app.py

The first run indexes ``docs/book.pdf`` into ``qdrant_db/``; later runs reuse it.
Delete ``qdrant_db/`` to force a rebuild.
"""

import os
import time
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()  # picks up OPENROUTER_API_KEY from a local .env, if present

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "docs" / "book.pdf"
DB_PATH = BASE_DIR / "qdrant_db"
COLLECTION_NAME = "my_documents"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3
MODEL = "openai/gpt-oss-120b:free"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 10

PROMPT_TEMPLATE = """You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not found in the context, say:
"I could not find this in the document."

==================================================

Context:
{context}

==================================================

Question:
{query}
"""


def get_api_key() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit(
            "Set OPENROUTER_API_KEY before running (get one at https://openrouter.ai/keys)."
        )
    return api_key


def build_vector_store() -> Qdrant:
    """Index the PDF into a local Qdrant store."""
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing source document: {PDF_PATH}")

    pages = PyPDFLoader(str(PDF_PATH)).load()
    print(f"Loaded PDF with {len(pages)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("Embedding model loaded")

    store = Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        path=str(DB_PATH),
        collection_name=COLLECTION_NAME,
    )
    print("Qdrant vector database created")
    return store


def answer(llm: ChatOpenAI, retriever, query: str) -> str:
    documents = retriever.invoke(query)
    print(f"Retrieved {len(documents)} relevant chunks")

    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = PROMPT_TEMPLATE.format(context=context, query=query)

    for attempt in range(MAX_RETRIES):
        try:
            return llm.invoke(prompt).content
        except Exception as exc:  # noqa: BLE001 - free tier rate limits
            print(f"Error: {exc}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)

    return "Model is busy. Please try again later."


def load_or_build_store() -> Qdrant:
    """Open the on-disk index if it exists, otherwise index the PDF."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if DB_PATH.exists() and any(DB_PATH.iterdir()):
        print(f"Reusing existing index at {DB_PATH}")
        try:
            return Qdrant.from_existing_collection(
                embedding=embeddings,
                path=str(DB_PATH),
                collection_name=COLLECTION_NAME,
            )
        except Exception as exc:  # noqa: BLE001 - stale/incompatible index
            print(f"Could not open the existing index ({exc}); rebuilding it.")

    return build_vector_store()


def main() -> None:
    api_key = get_api_key()
    store = load_or_build_store()

    retriever = store.as_retriever(search_kwargs={"k": TOP_K})

    llm = ChatOpenAI(
        model=MODEL,
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    print("LLM connected")

    while True:
        print("\n" + "=" * 50)
        query = input("\nAsk a question (type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break
        if not query:
            continue

        print("\n" + "=" * 50)
        print("\nANSWER:\n")
        print(answer(llm, retriever, query))
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
