from src.sdlccopilot.prompts.prompt_template import json_prompt_template
from src.sdlccopilot.prompts.qa_testing import qa_testing_system_prompt
from src.sdlccopilot.prompts.prompt_template import json_output_parser
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
from src.sdlccopilot.prompts.code import CODE_SYSTEM_PROMPT
from src.sdlccopilot.prompts.prompt_template import prompt_template
import sys

class QATestingHelper:
    def __init__(self, gemini_llm, anthropic_llm):
        self.gemini_llm = gemini_llm
        self.anthropic_llm = anthropic_llm
        
    def perform_qa_testing_with_llm(self, test_cases, backend_code):
        try:
            logging.info("Performing qa testing with LLM...")
            user_query =  f"Perform qa testing for the test cases {test_cases} for the this backend code: {backend_code}"
            chain = json_prompt_template | self.gemini_llm | json_output_parser
            response = chain.invoke({"system_prompt" : qa_testing_system_prompt, "human_query" : user_query})
            logging.info("QA testing performed with LLM.")
            logging.info(f"In perform_qa_testing_with_llm : {response}")
            return response
        except Exception as e:
            logging.error(f"Error performing qa testing: {str(e)}")
            raise CustomException(e, sys)

    def revised_backend_code_with_qa_testing_from_llm(self, code, test_cases, user_feedback):
        try:
            logging.info("Revising backend code according to qa testing with LLM...")
            user_query =  f"Analyze this backend code: {code} and fix these test cases {test_cases} according to the user feedback: {user_feedback} and return the revised code" 
            chain = prompt_template | self.anthropic_llm
            response = chain.invoke({"system_prompt" : CODE_SYSTEM_PROMPT, "human_query" : user_query})
            logging.info("Backend code revised according to qa testing with LLM.")
            logging.info(f"In revised_backend_code_with_qa_testing_from_llm : {response.content}")
            return response.content
        except Exception as e:
            logging.error(f"Error revising backend code according to qa testing: {str(e)}")
            raise CustomException(e, sys)
