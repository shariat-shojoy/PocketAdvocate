import os
import base64

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class VisionAnalyzer:

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

    def describe(self, image_path):

        image = self.encode_image(image_path)

        response = self.client.chat.completions.create(

            model=self.model,

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
                                "url": f"data:image/png;base64,{image}"
                            }
                        }

                    ]
                }
            ]

        )

        return response.choices[0].message.content