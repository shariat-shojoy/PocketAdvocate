from sentence_transformers import SentenceTransformer
import streamlit as st


@st.cache_resource
def load_embedding_model():
    print("Loading embedding model...")
    model = SentenceTransformer("intfloat/multilingual-e5-small")
    print("Embedding model loaded.")
    return model


class EmbeddingModel:

    def __init__(self):
        self.model = load_embedding_model()

    def encode(self, texts):

        texts = [f"passage: {t}" for t in texts]

        embeddings = self.model.encode(
            texts,
            batch_size=128,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings