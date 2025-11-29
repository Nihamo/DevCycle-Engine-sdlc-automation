from src.sdlccopilot.prompts.prompt_template import json_prompt_template, prompt_template
from src.sdlccopilot.prompts.user_story import generate_user_stories_system_prompt, revised_user_stories_system_prompt
from src.sdlccopilot.prompts.prompt_template import json_output_parser
from src.sdlccopilot.prompts.security_review import security_reviews_system_prompt
from src.sdlccopilot.prompts.code import CODE_SYSTEM_PROMPT
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class SecurityReviewHelper:
    def __init__(self, gemini_llm, anthropic_llm):
        self.gemini_llm = gemini_llm
        self.anthropic_llm = anthropic_llm
        
    def generate_security_reviews_from_llm(self, backend_code):
        try:
            logging.info("Generating security reviews with LLM...")
            user_query =  f"Analyze this backend code: {backend_code} and create the security reviews for the code" 
            chain = json_prompt_template | self.gemini_llm  | json_output_parser
            response = chain.invoke({"system_prompt" : security_reviews_system_prompt, "human_query" : user_query})
            logging.info(f"In generate_security_reviews_from_llm : {response}")
            logging.info("Security reviews generated with LLM.")
            return response
        except Exception as e:
            logging.error(f"Error generating security reviews: {str(e)}")
            raise CustomException(e, sys)

    def revised_backend_code_with_security_reviews_from_llm(self, code, reviews, user_feedback):
        try:
            logging.info("Revising backend code according to security reviews with LLM...")
            user_query = f"""EXISTING BACKEND CODE (PRESERVE ALL CODE NOT MENTIONED IN FEEDBACK):
{code}

SECURITY REVIEWS TO ADDRESS:
{reviews}

USER FEEDBACK (APPLY ONLY THESE CHANGES):
{user_feedback}

INSTRUCTIONS:
- Keep ALL existing files, modules, functions, and code that are NOT mentioned in the feedback
- Fix the security issues identified in the reviews
- Only modify the specific parts requested in the user feedback
- Return the complete codebase with all preserved code and security fixes applied"""
            chain = prompt_template | self.anthropic_llm
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code revised according to security reviews with LLM.")
            logging.info(f"In revised_backend_code_with_security_reviews_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising backend code according to security reviews: {str(e)}")
            raise CustomException(e, sys)