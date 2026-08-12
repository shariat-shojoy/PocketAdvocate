"""Multilingual embedding model shared by indexing and retrieval."""

import torch
from sentence_transformers import SentenceTransformer
import streamlit as st


# BGE-M3 supports Bengali and English retrieval well, and is easily within a
# 16 GB GPU.  It also accepts long legal passages (up to 8,192 tokens).
MODEL_NAME = "BAAI/bge-m3"


@st.cache_resource
def load_embedding_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading {MODEL_NAME} on {device}...")
    model = SentenceTransformer(MODEL_NAME, device=device)
    model.max_seq_length = 8192
    return model


class EmbeddingModel:
    def __init__(self):
        self.model = load_embedding_model()
        self.device = str(self.model.device)
        # 16 GB VRAM comfortably supports 32 BGE-M3 legal passages at once.
        self.batch_size = 32 if self.device.startswith("cuda") else 8

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
