from services.rag_pipeline import PocketAdvocate

assistant = PocketAdvocate()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = assistant.ask(question)

    print("\n")
    print(answer)
    print("\n")