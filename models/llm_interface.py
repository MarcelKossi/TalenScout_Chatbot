import os
import time
from openai import OpenAI, OpenAIError


class LLMInterface:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.2, max_retries=3):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing.")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries

    def _clean_output(self, response):
        try:
            return response.choices[0].message.content.strip()
        except Exception:
            return "Unexpected response format. Please try again."

    def generate_response(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        for _ in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=1000
                )
                return self._clean_output(response)

            except OpenAIError:
                time.sleep(1.2)

            except Exception:
                time.sleep(1.2)

        return "Technical difficulty: OpenAI API error."