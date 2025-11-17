from src.sdlccopilot.prompts.prompt_template import json_prompt_template
from src.sdlccopilot.prompts.prompt_template import json_output_parser
from src.sdlccopilot.prompts.test_cases import test_cases_system_prompt, revised_test_cases_system_prompt
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class TestCaseHelper:
    def __init__(self, llm):
        self.llm = llm
        
    def generate_test_cases_from_llm(self, functional_documents):
        try:
            logging.info("Generating test cases with LLM...")
            user_query =  f"Create test cases for the this project functional documentation: {functional_documents}" 
            chain = json_prompt_template | self.llm  | json_output_parser
            response = chain.invoke({"system_prompt" : test_cases_system_prompt, "human_query" : user_query})
            logging.info("Test cases generated with LLM.")
            logging.info(f"In generate_test_cases_from_llm : {response}")
            return response
        except Exception as e:
            logging.error(f"Error occurred while generating test cases: {str(e)}")
            raise CustomException(e, sys)
        
    def revised_test_cases_from_llm(self, test_cases, user_feedback):
        try:
            logging.info("Revising test cases with LLM...")
            user_query =  f"Revise these test cases {test_cases} with this user feedback {user_feedback}" 
            chain = json_prompt_template | self.llm  | json_output_parser
            response = chain.invoke({"system_prompt" : revised_test_cases_system_prompt, "human_query" : user_query})
            logging.info("Test cases revised with LLM.")
            logging.info(f"In revised_test_cases_from_llm : {response}")
            return response
        except Exception as e:
            logging.error(f"Error occurred while revising test cases: {str(e)}")
            raise CustomException(e, sys)
