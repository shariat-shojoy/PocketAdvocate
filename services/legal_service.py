from services.rag_pipeline import PocketAdvocate
from services.image_pipeline import ImageLegalAssistant


class LegalService:

    def __init__(self):
        self.text_pipeline = PocketAdvocate()
        self.image_pipeline = ImageLegalAssistant()

    def analyze_text(self, text):
        return self.text_pipeline.ask(text)

    def analyze_image(self, image_path):
        return self.image_pipeline.analyze(image_path)