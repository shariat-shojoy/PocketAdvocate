"""Multilingual embedding model shared by indexing and retrieval."""

import os
import torch
from sentence_transformers import SentenceTransformer
import streamlit as st


# Keep BGE-M3 locally for retrieval quality. Railway's standard CPU containers
# need a substantially smaller model to avoid an out-of-memory restart loop.
RAG_PROFILE = os.getenv("RAG_PROFILE", "local").lower()
PROFILE_CONFIG = {
    "local": {
        "model_name": "BAAI/bge-m3",
        "index_directory": "faiss_index",
        "max_seq_length": 8192,
    },
    "railway": {
        "model_name": "intfloat/multilingual-e5-small",
        "index_directory": "faiss_index_railway",
        "max_seq_length": 512,
    },
}
if RAG_PROFILE not in PROFILE_CONFIG:
    raise ValueError(f"Unknown RAG_PROFILE '{RAG_PROFILE}'. Use 'local' or 'railway'.")

MODEL_NAME = PROFILE_CONFIG[RAG_PROFILE]["model_name"]
INDEX_DIRECTORY = PROFILE_CONFIG[RAG_PROFILE]["index_directory"]
MAX_SEQUENCE_LENGTH = PROFILE_CONFIG[RAG_PROFILE]["max_seq_length"]


@st.cache_resource
def load_embedding_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading {MODEL_NAME} on {device}...")
    # Railway pre-downloads its smaller model during image build. Loading from
    # the local cache at runtime avoids repeated Hub checks during restarts.
    model = SentenceTransformer(
        MODEL_NAME,
        device=device,
        local_files_only=os.getenv("HF_LOCAL_FILES_ONLY", "0") == "1",
    )
    model.max_seq_length = MAX_SEQUENCE_LENGTH
    return model


class EmbeddingModel:
    def __init__(self):
        self.model = load_embedding_model()
        self.device = str(self.model.device)
        self.batch_size = 32 if self.device.startswith("cuda") else 4

    def _encode(self, texts):
        return self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def encode_documents(self, texts):
        return self._encode(texts)

    def encode_queries(self, texts):
        return self._encode(texts)
