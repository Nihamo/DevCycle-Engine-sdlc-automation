from src.sdlccopilot.prompts.prompt_template import prompt_template
from src.sdlccopilot.prompts.code import CODE_SYSTEM_PROMPT, FRONTEND_PROMPT, BACKEND_PROMPT
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class CodeHelper:
    def __init__(self, llm):
        self.llm = llm
    
    def generate_frontend_code_from_llm(self, user_stories):
        try:
            logging.info("Generating frontend code with LLM...")
            user_query =  f"Analyze these user stories {user_stories} and generate a frontend react + vite code. {FRONTEND_PROMPT}."
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Frontend code generated with LLM.")
            logging.info(f"In generate_frontend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating frontend code: {str(e)}")
            raise CustomException(e, sys)

    def revised_frontend_code_from_llm(self, code, user_feedback):
        try:
            logging.info("Revising frontend code with LLM...")
            user_query =  f"Analyze this React frontend code: {code} and revise it according to user feedback: {user_feedback} and {FRONTEND_PROMPT}."
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Frontend code revised with LLM.")
            logging.info(f"In revised_frontend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising frontend code: {str(e)}")
            raise CustomException(e, sys)
    
    def generate_backend_code_from_llm(self, user_stories):
        try:
            logging.info("Generating backend code with LLM...")
            user_query =  f"Analyze these user stories {user_stories} and generate a nodejs backend code. {BACKEND_PROMPT}."
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code generated with LLM.")
            logging.info(f"In generate_backend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating backend code: {str(e)}")
            raise CustomException(e, sys)
    
    def revised_backend_code_from_llm(self, code, user_feedback):
        try:
            logging.info("Revising backend code with LLM...")
            user_query =  f"Analyze this backend code: {code} and revise it according to user feedback: {user_feedback} and {BACKEND_PROMPT}."
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code revised with LLM.")
            logging.info(f"In revised_backend_code_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising backend code: {str(e)}")
            raise CustomException(e, sys)


