from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("intfloat/multilingual-e5-small")
        print("Embedding model loaded.")

    def encode(self, texts):
        texts = [f"passage: {t}" for t in texts]

        embeddings = self.model.encode(
            texts,
            batch_size=128,          # Increase batch size
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings