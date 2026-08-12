import os
from dotenv import load_dotenv
from openai import OpenAI

from config.prompt import SYSTEM_PROMPT

load_dotenv()


class LegalLLM:

    MAX_OUTPUT_TOKENS = 1_500
    MAX_HISTORY_TURNS = 6
    MAX_CONTEXT_CHARACTERS = 18_000

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
            max_tokens=self.MAX_OUTPUT_TOKENS,
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

    def generate_stream(self, query, context):
        prompt = f"""
    User Incident:

    {query}

    ----------------------------------------

    Retrieved Bangladesh Laws:

    {context}
    """

        stream = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            max_tokens=self.MAX_OUTPUT_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            if content:
                yield content

    def generate_chat_stream(self, history, query, context):
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Append previous conversation history
        # Keep only recent turns. This avoids progressively larger requests as
        # a conversation continues and protects the provider context budget.
        for msg in history[-self.MAX_HISTORY_TURNS:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ["user", "assistant"] and content:
                messages.append({
                    "role": role,
                    "content": content
                })

        # Append current user prompt with retrieved context
        user_prompt = f"""
Current User Inquiry:
{query}

----------------------------------------
Retrieved Relevant Bangladesh Laws:
{context[:self.MAX_CONTEXT_CHARACTERS]}
"""
        messages.append({
            "role": "user",
            "content": user_prompt
        })

        stream = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            max_tokens=self.MAX_OUTPUT_TOKENS,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            if content:
                yield content

