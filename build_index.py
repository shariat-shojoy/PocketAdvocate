"""Build the FAISS index from every JSON statute in data/."""

import pickle
from pathlib import Path

import faiss

from models.embedding import EmbeddingModel, MODEL_NAME
from utils.chunker import dataframe_to_documents
from utils.loader import LawLoader


BASE_DIR = Path(__file__).resolve().parent
INDEX_DIR = BASE_DIR / "data" / "faiss_index"


def main():
    dataframe = LawLoader(BASE_DIR / "data").load()
    documents, metadata = dataframe_to_documents(dataframe)
    print(f"Loaded {len(dataframe)} statute records into {len(documents)} retrieval passages.")

    embedder = EmbeddingModel()
    print(f"Embedding with {MODEL_NAME} on {embedder.device}.")
    embeddings = embedder.encode_documents(documents)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    print(f"Indexed {index.ntotal} passages ({embeddings.shape[1]} dimensions).")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / "law.index"))
    with (INDEX_DIR / "metadata.pkl").open("wb") as file:
        pickle.dump({
            "documents": documents,
            "metadata": metadata,
            "embedding_model": MODEL_NAME,
        }, file)
    print(f"Index written to {INDEX_DIR}.")


if __name__ == "__main__":
    main()
