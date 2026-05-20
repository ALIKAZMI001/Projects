import os
import time

# ==========================================
# PDF LOADER
# ==========================================

from langchain_community.document_loaders import PyPDFLoader

# ==========================================
# TEXT SPLITTER
# ==========================================

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# HUGGINGFACE EMBEDDINGS
# ==========================================

from langchain_huggingface import HuggingFaceEmbeddings

# ==========================================
# OPENROUTER MODEL
# ==========================================

from langchain_openai import ChatOpenAI

# ==========================================
# QDRANT VECTOR DATABASE
# ==========================================

from langchain_community.vectorstores import Qdrant

# ==========================================
# OPENROUTER API KEY
# ==========================================

os.environ["OPENAI_API_KEY"] = "................"

# ==========================================
# LOAD PDF
# ==========================================

loader = PyPDFLoader("docs/book.pdf")

docs = loader.load()

print(f"\nLoaded PDF with {len(docs)} pages")

# ==========================================
# SPLIT DOCUMENT INTO CHUNKS
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

print(f"Created {len(chunks)} chunks")

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("\nEmbedding model loaded")

# ==========================================
# CREATE QDRANT VECTOR STORE
# ==========================================

qdrant = Qdrant.from_documents(
    documents=chunks,
    embedding=embeddings,
    path="./qdrant_db",
    collection_name="my_documents"
)

print("\nQdrant vector database created")

# ==========================================
# CREATE RETRIEVER
# ==========================================

retriever = qdrant.as_retriever(
    search_kwargs={"k": 3}
)

print("\nRetriever ready")

# ==========================================
# CONNECT TO FREE OPENROUTER MODEL
# ==========================================

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",

    # You can also use:
    # model="google/gemma-4-31b-it:free",

    base_url="https://openrouter.ai/api/v1",

    api_key=os.environ["OPENAI_API_KEY"]
)

print("\nFree LLM connected")

# ==========================================
# CHAT LOOP
# ==========================================

while True:

    print("\n" + "=" * 50)

    query = input("\nAsk a question (type 'exit' to quit): ")

    # ==========================================
    # EXIT CONDITION
    # ==========================================

    if query.lower() == "exit":

        print("\nGoodbye!")

        break

    # ==========================================
    # RETRIEVE RELEVANT DOCUMENTS
    # ==========================================

    results = retriever.invoke(query)

    print(f"\nRetrieved {len(results)} relevant chunks")

    # ==========================================
    # BUILD CONTEXT
    # ==========================================

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    # ==========================================
    # CREATE PROMPT
    # ==========================================

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not found in the context,
say:

"I could not find this in the document."

==================================================

Context:
{context}

==================================================

Question:
{query}
"""

    # ==========================================
    # GENERATE RESPONSE WITH RETRY
    # ==========================================

    max_retries = 3

    response = None

    for attempt in range(max_retries):

        try:

            response = llm.invoke(prompt)

            break

        except Exception as e:

            print(f"\nError: {e}")

            if attempt < max_retries - 1:

                print("\nRetrying in 10 seconds...")

                time.sleep(10)

            else:

                print("\nModel is busy. Please try again later.")

    # ==========================================
    # PRINT RESPONSE
    # ==========================================

    if response:

        print("\n" + "=" * 50)

        print("\nANSWER:\n")

        print(response.content)

        print("\n" + "=" * 50)