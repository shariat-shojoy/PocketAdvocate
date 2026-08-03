# ⚖️ PocketAdvocate
### AI-Powered Legal Assistant for Bangladesh

PocketAdvocate is an AI-powered legal assistant that helps Bangladeshi citizens understand potential legal issues by analyzing **text descriptions** or **images** of incidents. It combines **Vision-Language Models (VLMs)**, **Retrieval-Augmented Generation (RAG)**, and **Large Language Models (LLMs)** to retrieve relevant Bangladeshi laws and generate understandable legal guidance.

---

## 📌 Features

- 📝 Analyze legal incidents from text
- 🖼 Analyze screenshots or images using Vision Language Models
- 📚 Retrieve relevant Bangladesh laws using semantic search
- 🤖 AI-generated legal explanation
- ⚖️ Suggest applicable laws and next legal steps
- 🎯 Human-Computer Interaction (HCI) based user interface
- 🌐 Deployable on Railway 

- 🌐 Live link: https://pocketadvocate-production.up.railway.app/

---
<img width="2559" height="1150" alt="image" src="https://github.com/user-attachments/assets/55b0fdb8-a77e-44ab-b54e-08f3a2a309b5" />

---
<img width="2558" height="978" alt="image" src="https://github.com/user-attachments/assets/55c4d7a9-85ee-47a3-b16f-2303db9f0ffc" />

---
<img width="2550" height="1220" alt="image" src="https://github.com/user-attachments/assets/d1cd857c-23e9-493f-ae03-2398107b4c27" />

---





# 🏗 System Architecture

```text
                User
                  │
                  ▼
          Streamlit Web UI
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
 Text Description      Image Upload
        │                    │
        │             Qwen2.5-VL
        │          (Image Understanding)
        │                    │
        └──────────┬─────────┘
                   ▼
        Unified Incident Description
                   │
                   ▼
       SentenceTransformer Embedding
         (all-MiniLM-L6-v2)
                   │
                   ▼
          FAISS Vector Search
                   │
                   ▼
      Bangladesh Law Knowledge Base
                   │
                   ▼
      Retrieval-Augmented Generation
                   │
                   ▼
      Groq API (Llama Model)
                   │
                   ▼
      Legal Advice & Recommendations
                   │
                   ▼
         Streamlit Results Page
```

---

# 🚀 Workflow

## 1. User Input

The user provides either:

- A text description of the incident
- An image or screenshot

---

## 2. Image Understanding (Optional)

If an image is uploaded:

- Qwen2.5-VL analyzes the image.
- Extracts important legal context.
- Produces a textual description of the incident.

---

## 3. Embedding Generation

The incident description is converted into semantic embeddings using:

- Sentence Transformers
- all-MiniLM-L6-v2

---

## 4. Semantic Search

The embedding is searched against a FAISS vector database built from Bangladeshi law documents.

Top-K relevant laws are retrieved.

---

## 5. RAG

The retrieved legal sections are combined with the user's incident.

A prompt is created for the LLM.

---

## 6. AI Legal Reasoning

The prompt is sent to

- Groq API
- Llama Model

The model generates

- Relevant laws
- Legal explanation
- Recommended next actions

---

## 7. Results

The user receives

- Relevant Bangladesh laws
- AI legal explanation
- Suggested legal actions

---

# 🧠 Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Programming Language | Python |
| Vision Language Model | Qwen2.5-VL |
| Embedding Model | SentenceTransformers |
| Embedding | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Knowledge Retrieval | RAG |
| Large Language Model | Llama (via Groq API) |
| Data Processing | Pandas |
| Image Processing | Pillow |
| Environment | python-dotenv |
| Version Control | Git |
| Repository | GitHub |
| Deployment | Railway / Streamlit Cloud |

---

# 📂 Project Structure

```
PocketAdvocate/
│
├── app.py
├── requirements.txt
├── .env
│
├── components/
│   ├── hero.py
│   ├── navbar.py
│   └── wizard.py
│
├── services/
│   ├── legal_service.py
│   ├── rag_pipeline.py
│   └── image_pipeline.py
│
├── models/
│   ├── retriever.py
│   ├── llm.py
│   └── embedding.py
│
├── data/
│   ├── laws.csv
│   └── faiss_index/
│       ├── law.index
│       └── metadata.pkl
│
├── outputs/
│
└── assets/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/PocketAdvocate.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run

```bash
streamlit run app.py
```

---

# 📊 Core Technologies

- Python
- Streamlit
- Qwen2.5-VL
- Sentence Transformers
- FAISS
- Retrieval-Augmented Generation (RAG)
- Groq API
- Llama
- Git
- GitHub

---

# 💡 Future Improvements

- Voice-based legal reporting
- Bengali Speech-to-Text
- Court document generation
- Evidence timeline generation
- Citation of Bangladesh Penal Code sections
- Multi-language support
- Mobile application

---

# 📜 Disclaimer

PocketAdvocate provides AI-assisted legal guidance for educational and informational purposes only. It does not replace advice from a licensed legal professional.

---

# 👨‍💻 Author

**Shariat Shojoy**

Department of Computer Science & Engineering

AI • Machine Learning • Computer Vision • Natural Language Processing
