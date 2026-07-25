from models.retriever import LawRetriever

retriever = LawRetriever()

query = input("Enter your legal query: ")

results = retriever.search(query)

print("\n" + "=" * 80)

for i, item in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(f"Similarity : {item['score']:.3f}")

    print("-" * 60)

    print(item["document"][:800])

    print("-" * 60)