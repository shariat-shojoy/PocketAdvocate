# Pocket Advocate

Pocket Advocate is a multilingual Bangladesh-law research assistant. It accepts questions in Bangla or English, optionally analyzes one or more evidence images, retrieves relevant statutory passages, and produces a structured, source-aware explanation.

> **Disclaimer:** This project provides educational legal information, not legal advice. For a decision about a real matter, consult a qualified advocate in Bangladesh.

## What it does

- Answers legal questions in Bangla or English.
- Accepts multiple uploaded images and camera captures with a single message.
- Uses a vision model to turn image evidence into factual incident descriptions.
- Searches a FAISS index built from Bangladesh law JSON files.
- Shows the law title, section/article, and source file in the retrieval context used for answers.
- Keeps a short conversation history for follow-up questions without allowing requests to grow indefinitely.

## RAG pipeline

```text
Question + optional evidence images
                |
                +--> OpenRouter / Qwen2.5-VL (image description)
                |
                v
     Multilingual query (Bangla or English)
                |
                v
  BAAI/bge-m3 embeddings --> FAISS similarity search
                |
                v
  Source-aware Bangladesh law passages
                |
                v
 Groq / Llama 3.3 70B --> structured legal explanation
```

## Legal data

The index is built from the JSON files in `data/`, currently including:

- Constitution of Bangladesh
- Penal Code
- Code of Criminal Procedure
- Registration Act
- State Acquisition and Tenancy material
- Transfer of Property Act

Each indexed passage retains metadata for the law title, section/article, chapter/part, original JSON source file, source-record number, and chunk number. Long provisions are split with overlap so that retrieval remains precise while preserving surrounding context.

## Tech stack

| Area | Technology |
| --- | --- |
| Web application | Streamlit |
| Embeddings | `BAAI/bge-m3` via SentenceTransformers |
| Vector search | FAISS (`IndexFlatIP`) |
| Legal response model | `llama-3.3-70b-versatile` via Groq |
| Image understanding | `qwen/qwen2.5-vl-72b-instruct` via OpenRouter |
| Data format | JSON statutes with pandas normalization |

## Requirements

- Python 3.13 (the included environment was tested with Python 3.13).
- Groq API key for legal-answer generation.
- OpenRouter API key if image analysis is enabled.
- Internet access the first time BGE-M3 is downloaded.
- Optional: NVIDIA GPU. The repository installs CPU-compatible PyTorch so it can deploy to Railway. For local GPU acceleration, install the CUDA PyTorch wheel matching your NVIDIA driver after installing the project. The app automatically uses CUDA when it is available.

## Installation

```powershell
git clone https://github.com/shariat-shojoy/PocketAdvocate.git
cd PocketAdvocate
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Never commit `.env` or API keys. If a key was ever exposed, revoke it from the provider and create a replacement.

## Build or rebuild the legal index

Whenever you add, remove, or change a JSON file in `data/`, rebuild the index:

```powershell
python build_index.py
```

This creates or replaces:

```text
data/faiss_index/law.index
data/faiss_index/metadata.pkl
```

The build script automatically reads every `data/*.json` statute, chunks long provisions, embeds the chunks with BGE-M3, and writes their metadata alongside the FAISS index.

To check whether PyTorch can see the GPU:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

## Run the application

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Railway deployment

Railway runs this project on CPU. The included `nixpacks.toml` installs Python 3.11, pre-downloads the deployment embedding model, and starts Streamlit on Railway's assigned port. It uses the `railway` RAG profile (`intfloat/multilingual-e5-small` plus `data/faiss_index_railway/`) to fit a smaller cloud memory budget; local runs retain BGE-M3 by default.

Set these Railway service variables before deploying:

```text
GROQ_API_KEY
OPENROUTER_API_KEY
```

Commit and push `requirements.txt`, `nixpacks.toml`, and both FAISS index directories (`data/faiss_index/` and `data/faiss_index_railway/`). Do not deploy `.env`, `uploads/`, or `outputs/`.

## Using the app

1. Write a question in Bangla or English.
2. Optionally upload several images, take a new camera photo, or use both.
3. Review or remove individual evidence images before sending.
4. Read the structured answer and referenced law passages.
5. Ask a follow-up question; the most recent conversation turns are retained for context.

Image descriptions are limited to 700 output tokens and legal responses to 1,500 output tokens to keep OpenRouter/Groq requests predictable.

## Project structure

```text
PocketAdvocate/
|-- app.py                         # Streamlit entry point
|-- build_index.py                 # JSON statutes -> FAISS index
|-- data/
|   |-- *.json                     # Bangladesh-law source files
|   `-- faiss_index/               # Generated index and metadata
|-- models/
|   |-- embedding.py               # BGE-M3 model configuration
|   |-- retriever.py               # FAISS retrieval + source citations
|   |-- llm.py                     # Groq legal-answer client
|   `-- vision.py                  # OpenRouter image-analysis client
|-- services/
|   |-- legal_service.py           # Unified text/image request handling
|   |-- rag_pipeline.py            # Text RAG flow
|   `-- image_pipeline.py          # Image RAG flow
|-- components/
|   `-- chat_interface.py          # Conversation and multi-image UI
|-- utils/
|   |-- loader.py                  # JSON loading
|   `-- chunker.py                 # Passage construction and chunking
`-- assets/css/style.css            # Interface styling
```

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `Legal index is missing` | Run `python build_index.py`. |
| Index uses a different embedding model | Rebuild with `python build_index.py`. |
| OpenRouter 402 / insufficient credits | Add credits or lower the limits in `models/vision.py`; the app already caps vision output at 700 tokens. |
| GPU is not detected | Confirm NVIDIA drivers are installed and install the CUDA-enabled PyTorch wheel from `requirements.txt`. CPU indexing still works, but is slower. |
| Hugging Face download fails | Check internet/proxy access, then rerun `python build_index.py`. |

## License and attribution

Review the licences and terms of the source legal datasets and external model/API providers before redistribution or production deployment.
