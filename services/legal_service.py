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