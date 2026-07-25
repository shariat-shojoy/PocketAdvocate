import os
import pickle
import faiss

from utils.loader import LawLoader
from utils.chunker import dataframe_to_documents
from models.embedding import EmbeddingModel

# -----------------------------
# Load Dataset
# -----------------------------

loader = LawLoader("data/bdlaws_formatted.csv")
df = loader.load()

documents, metadata = dataframe_to_documents(df)

print(f"Loaded {len(documents)} legal documents.")

# -----------------------------
# Generate Embeddings
# -----------------------------

embedder = EmbeddingModel()

embeddings = embedder.encode(documents)

dimension = embeddings.shape[1]

# -----------------------------
# Build FAISS
# -----------------------------

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(f"Indexed {index.ntotal} documents.")

# -----------------------------
# Save
# -----------------------------

os.makedirs("data/faiss_index", exist_ok=True)

faiss.write_index(
    index,
    "data/faiss_index/law.index"
)

with open("data/faiss_index/metadata.pkl", "wb") as f:
    pickle.dump(
        {
            "documents": documents,
            "metadata": metadata
        },
        f
    )

print("Done.")