import os
import openai
from config import Config

OPENAI_API_KEY = Config.OPENAI_API_KEY
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

class LLMService:
    def __init__(self, model='gpt-4o-mini'):
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        if not OPENAI_API_KEY:
            return '[LLM not configured] set OPENAI_API_KEY to use full capabilities.'
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{'role':'system','content':'You are a helpful agronomy assistant.'},
                      {'role':'user','content':prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp['choices'][0]['message']['content'].strip()
