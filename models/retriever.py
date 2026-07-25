import pickle
import faiss

from models.embedding import EmbeddingModel


class LawRetriever:

    def __init__(self):

        print("Loading FAISS index...")

        self.index = faiss.read_index("data/faiss_index/law.index")

        with open("data/faiss_index/metadata.pkl", "rb") as f:
            data = pickle.load(f)

        self.documents = data["documents"]
        self.metadata = data["metadata"]

        self.embedder = EmbeddingModel()

        print("Retriever ready.")

    def search(self, query, top_k=5):

        query_embedding = self.embedder.encode(
            [f"query: {query}"]
        )

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            meta = self.metadata[idx]

            result = {
                "score": float(score),
                "law_title": meta.get("law_title", ""),
                "section_name": meta.get("section_name", ""),
                "url_id": meta.get("url_id", ""),
                "document": self.documents[idx]
            }

            results.append(result)

        return results