from models.retriever import LawRetriever
from models.llm import LegalLLM
from services.rag_pipeline import PocketAdvocate
from services.image_pipeline import ImageLegalAssistant


class LegalService:

    def __init__(self):

        # Loaded exactly once here — this is the single copy of the
        # embedding model + FAISS index shared by both pipelines below.
        # Previously each pipeline built its own LawRetriever(), which
        # loaded the model and index twice per LegalService() call.
        self.retriever = LawRetriever()
        self.llm = LegalLLM()

        self.text_pipeline = PocketAdvocate(self.retriever, self.llm)
        self.image_pipeline = ImageLegalAssistant(self.retriever, self.llm)

    def analyze_text(self, text):
        return self.text_pipeline.ask(text)

    def analyze_image(self, image_path):
        return self.image_pipeline.analyze(image_path)

    def analyze_unified_stream(self, text=None, image_path=None):
        if image_path:
            yield from self.image_pipeline.analyze_stream(image_path, extra_text=text or "")
        elif text:
            yield from self.text_pipeline.ask_stream(text)
        else:
            yield "**⚡ Key Takeaway:** Please provide text or an image input to analyze."

    def analyze_chat_stream(self, history, text=None, image_paths=None):
        query = text or ""
        image_paths = image_paths or []
        vision_descriptions = []

        for image_number, image_path in enumerate(image_paths, start=1):
            description = self.image_pipeline.vision.describe(image_path)
            vision_descriptions.append(f"Image {image_number}:\n{description}")

        if vision_descriptions:
            visual_evidence = "\n\n".join(vision_descriptions)
            query = (
                f"Visual Evidence Details:\n{visual_evidence}"
                f"\n\nUser Question:\n{text or ''}"
            )

        if vision_descriptions:
            with open("outputs/image_analysis.txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join(vision_descriptions))

        retrieved = self.retriever.search(query, top_k=5)
        context_list = []
        for i, law in enumerate(retrieved, start=1):
            context_list.append(
                f"Law #{i} — Source: {law['citation']}\nText:\n{law['document']}"
            )
        context = "\n\n".join(context_list)

        with open("outputs/retrieved_context.txt", "w", encoding="utf-8") as f:
            f.write(context)

        yield from self.llm.generate_chat_stream(history, query, context)

