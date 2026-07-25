from services.image_pipeline import ImageLegalAssistant

assistant = ImageLegalAssistant()

image = "E:/pocket_advocate/uploads/one.png"

answer = assistant.analyze(image)

print("\n")
print(answer)