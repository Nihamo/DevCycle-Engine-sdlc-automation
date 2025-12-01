
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Try both GEMINI_API_KEY and GOOGLE_API_KEY for compatibility
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

class GeminiLLM:
    def __init__(self, model_name):
        self.model_name = model_name
        pass

    def get(self):
        # Ensure GOOGLE_API_KEY is set in environment to prevent service account lookup
        # This is critical for serverless environments where credentials files don't exist
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable must be set")
        
        # Set GOOGLE_API_KEY in environment (ChatGoogleGenerativeAI checks this)
        os.environ['GOOGLE_API_KEY'] = api_key
        
        # Unset GOOGLE_APPLICATION_CREDENTIALS if set to prevent service account lookup
        # This ensures we use API key authentication instead of service account credentials
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        
        # Use api_key parameter explicitly to force API key authentication
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key  # Explicitly pass API key to prevent service account lookup
        )