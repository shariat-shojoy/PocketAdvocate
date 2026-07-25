import os
from dotenv import load_dotenv
from openai import OpenAI

from config.prompt import SYSTEM_PROMPT

load_dotenv()


class LegalLLM:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        # Change this to any model available in your Groq account
        self.model = "llama-3.3-70b-versatile"

    def generate(self, query, context):

        prompt = f"""
    User Incident:

    {query}

    ----------------------------------------

    Retrieved Bangladesh Laws:

    {context}
    """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content