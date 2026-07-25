from pathlib import Path

from models.vision import VisionAnalyzer
from models.retriever import LawRetriever
from models.llm import LegalLLM


class ImageLegalAssistant:

    def __init__(self):

        self.vision = VisionAnalyzer()
        self.retriever = LawRetriever()
        self.llm = LegalLLM()

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