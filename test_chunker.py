from utils.loader import LawLoader
from utils.chunker import dataframe_to_documents

loader = LawLoader("data/bdlaws_formatted.csv")

df = loader.load()

docs, metadata = dataframe_to_documents(df)

print(docs[0])

print("=" * 60)

print(metadata[0])