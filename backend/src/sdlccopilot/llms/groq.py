from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()   

api_key = os.getenv("GROQ_API_KEY")

class GroqLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def get(self):
        return ChatGroq(model=self.model_name, api_key=api_key)