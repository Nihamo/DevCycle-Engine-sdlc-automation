
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

class AnthropicLLM:
    def __init__(self, model_name):
        self.model_name = model_name
        pass

    def get(self):
        return ChatAnthropic(
            model= self.model_name,
            temperature=0,
            max_tokens=8000,
            max_retries=2,  
            api_key=api_key
        )
    