# RAG PDF Chatbot

Ask questions about a PDF and get answers grounded **only** in that document. If the
answer isn't in the text, the model says so instead of inventing one.

```
docs/book.pdf
     │  PyPDFLoader
     ▼
 pages ──► RecursiveCharacterTextSplitter (500 chars, 100 overlap)
     │
     ▼
 chunks ──► all-MiniLM-L6-v2 embeddings ──► Qdrant (local, on disk)
                                                    │
 question ──► embed ──► top-3 similarity search ─────┘
                              │
                              ▼
                    prompt = context + question
                              │
                              ▼
                   OpenRouter chat model → answer
```

## Why these pieces

| Choice | Reason |
| --- | --- |
| `RecursiveCharacterTextSplitter` (500/100) | Keeps paragraphs intact while giving each chunk enough context |
| `all-MiniLM-L6-v2` | Small, fast, runs locally — no embedding API cost |
| Qdrant on disk | Persistent index; re-runs don't re-embed the PDF |
| `k = 3` | Enough context for a book-length document without blowing the prompt |
| Grounded prompt | Explicitly instructs the model to refuse rather than hallucinate |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
$env:OPENROUTER_API_KEY="sk-or-..."
python app.py
```

Or put it in a `.env` file in this folder (`OPENROUTER_API_KEY=sk-or-...`) — it is
loaded automatically via `python-dotenv`.

## Usage

```
Ask a question (type 'exit' to quit): what is the main argument of chapter 2?
```

The first run indexes `docs/book.pdf` into `qdrant_db/`. Later runs reopen the
existing collection (`Qdrant.from_existing_collection`) — delete `qdrant_db/` to
force a rebuild. Swap in your own PDF by replacing `docs/book.pdf`.

## Implementation notes

- Retrieval and generation are separate steps, so the retrieved chunks are printed
  (`Retrieved N relevant chunks`) — useful for checking *why* an answer came out the
  way it did.
- The free OpenRouter model is rate-limited; `answer()` retries three times with a
  10 s backoff and returns a clear message instead of raising.
- The prompt is templated and pinned to the retrieved context, which is what keeps
  the bot from answering outside the document.

## Stack

`langchain` · `langchain-community` · `langchain-huggingface` · `qdrant-client` ·
`sentence-transformers` · `pypdf` · OpenRouter
