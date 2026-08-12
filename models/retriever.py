"""FAISS retrieval for the JSON statute collection."""

import pickle
from pathlib import Path

import faiss

from models.embedding import EmbeddingModel, MODEL_NAME


class LawRetriever:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        index_dir = base_dir / "data" / "faiss_index"
        index_path = index_dir / "law.index"
        metadata_path = index_dir / "metadata.pkl"
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("Legal index is missing. Run `python build_index.py` first.")

        self.index = faiss.read_index(str(index_path))
        with metadata_path.open("rb") as file:
            data = pickle.load(file)
        if data.get("embedding_model") != MODEL_NAME:
            raise RuntimeError(
                "The legal index uses a different embedding model. Run `python build_index.py` to rebuild it."
            )

        self.documents = data["documents"]
        self.metadata = data["metadata"]
        self.embedder = EmbeddingModel()
        print(f"Retriever ready: {self.index.ntotal} passages from JSON statutes.")

    def search(self, query, top_k=5):
        top_k = min(max(1, top_k), self.index.ntotal)
        query_embedding = self.embedder.encode_queries([query])
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            meta = self.metadata[idx]
            result = {
                "score": float(score),
                "law_title": meta.get("law_title", ""),
                "section_name": meta.get("section_name", ""),
                "section_number": meta.get("section_number", ""),
                "chapter": meta.get("chapter", ""),
                "source_file": meta.get("source_file", ""),
                "source_record": meta.get("source_record", ""),
                "chunk_number": meta.get("chunk_number", ""),
                "citation": self._citation(meta),
                "document": self.documents[idx],
            }
            results.append(result)
        return results

    @staticmethod
    def _citation(meta):
        section = meta.get("section_name") or "Unnumbered provision"
        source = meta.get("source_file") or "JSON statute source"
        return f"{meta.get('law_title', 'Untitled law')} — {section} ({source})"
