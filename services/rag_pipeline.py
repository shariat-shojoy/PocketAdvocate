from pathlib import Path


class PocketAdvocate:

    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def ask(self, question):

        retrieved = self.retriever.search(question)

        context = []

        for i, law in enumerate(retrieved, start=1):

            context.append(
                f"""
Relevant Law #{i}

Source / Citation:
{law['citation']}

Law Title:
{law['law_title']}

Section:
{law['section_name']}

Similarity Score:
{law['score']:.4f}

Legal Text:
{law['document']}
"""
            )

        context = "\n\n".join(context)

        # ---------- Save retrieved context ----------
        Path("outputs").mkdir(exist_ok=True)

        with open(
            "outputs/retrieved_context.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(f"User Query:\n{question}\n\n")
            f.write("=" * 120 + "\n\n")
            f.write(context)

        # ---------- Ask LLM ----------
        answer = self.llm.generate(question, context)

        # ---------- Save final answer ----------
        with open(
            "outputs/final_response.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(f"User Query:\n{question}\n\n")
            f.write("=" * 120 + "\n\n")
            f.write(answer)

        return answer

    def ask_stream(self, question):
        retrieved = self.retriever.search(question)

        context_list = []
        for i, law in enumerate(retrieved, start=1):
            context_list.append(
                f"""
Relevant Law #{i}

Source / Citation:
{law['citation']}

Law Title:
{law['law_title']}

Section:
{law['section_name']}

Similarity Score:
{law['score']:.4f}

Legal Text:
{law['document']}
"""
            )

        context = "\n\n".join(context_list)

        Path("outputs").mkdir(exist_ok=True)
        with open("outputs/retrieved_context.txt", "w", encoding="utf-8") as f:
            f.write(f"User Query:\n{question}\n\n")
            f.write("=" * 120 + "\n\n")
            f.write(context)

        full_answer = []
        for chunk in self.llm.generate_stream(question, context):
            full_answer.append(chunk)
            yield chunk

        complete_answer = "".join(full_answer)
        with open("outputs/final_response.txt", "w", encoding="utf-8") as f:
            f.write(f"User Query:\n{question}\n\n")
            f.write("=" * 120 + "\n\n")
            f.write(complete_answer)
