from pathlib import Path

from models.vision import VisionAnalyzer


class ImageLegalAssistant:

    def __init__(self, retriever, llm):

        self.vision = VisionAnalyzer()
        self.retriever = retriever
        self.llm = llm

        Path("outputs").mkdir(exist_ok=True)

    def analyze(self, image_path):

        print("Analyzing image...")

        incident = self.vision.describe(image_path)

        with open(
            "outputs/image_analysis.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(incident)

        print("Searching laws...")

        retrieved = self.retriever.search(
            incident,
            top_k=5
        )

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

Similarity:
{law['score']:.4f}

Law Text:
{law['document']}
"""
            )

        context = "\n".join(context)

        with open(
            "outputs/retrieved_context.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(context)

        print("Generating answer...")

        answer = self.llm.generate(
            incident,
            context
        )

        with open(
            "outputs/final_response.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(answer)

        return answer

    def analyze_stream(self, image_path, extra_text=""):
        print("Analyzing image with vision model...")
        vision_description = self.vision.describe(image_path)

        with open("outputs/image_analysis.txt", "w", encoding="utf-8") as f:
            f.write(vision_description)

        combined_query = vision_description
        if extra_text and extra_text.strip():
            combined_query = f"Visual Evidence Details:\n{vision_description}\n\nAdditional User Details:\n{extra_text.strip()}"

        print("Searching laws...")
        retrieved = self.retriever.search(combined_query, top_k=5)

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

Similarity:
{law['score']:.4f}

Law Text:
{law['document']}
"""
            )

        context = "\n".join(context_list)

        with open("outputs/retrieved_context.txt", "w", encoding="utf-8") as f:
            f.write(context)

        print("Streaming answer...")
        full_answer = []
        for chunk in self.llm.generate_stream(combined_query, context):
            full_answer.append(chunk)
            yield chunk

        complete_answer = "".join(full_answer)
        with open("outputs/final_response.txt", "w", encoding="utf-8") as f:
            f.write(complete_answer)
