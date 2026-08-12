import os
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class VisionAnalyzer:

    # Image descriptions only need a short factual summary. Keeping this low
    # prevents OpenRouter from reserving the model's 65,536-token default.
    MAX_OUTPUT_TOKENS = 700

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

        self.model = "qwen/qwen2.5-vl-72b-instruct"

    def encode_image(self, image_path):

        with open(image_path, "rb") as f:
            return base64.b64encode(
                f.read()
            ).decode("utf-8")

    @staticmethod
    def image_media_type(image_path):
        extension = Path(image_path).suffix.lower()
        return {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(extension, "image/png")

    def describe(self, image_path):

        image = self.encode_image(image_path)

        response = self.client.chat.completions.create(

            model=self.model,
            max_tokens=self.MAX_OUTPUT_TOKENS,
            temperature=0,

            messages=[
                {
                    "role": "user",
                    "content": [

                        {
                            "type": "text",
                            "text": """
You are an expert incident analyst.

Analyze the uploaded image.

Determine whether it is:

1. Social media screenshot
2. Chat screenshot
3. Legal document
4. Photo
5. Government notice
6. News article
7. Other

Then write a factual description of the incident.

Mention:

- violence
- threats
- fraud
- harassment
- abusive language
- property damage
- accident
- contract
- official notice

Do NOT explain any law.

Do NOT give legal advice.

Output only plain text.
"""
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{self.image_media_type(image_path)};base64,{image}"
                            }
                        }

                    ]
                }
            ]

        )

        return response.choices[0].message.content
