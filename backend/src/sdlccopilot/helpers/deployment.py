from src.sdlccopilot.prompts.prompt_template import prompt_template
from src.sdlccopilot.prompts.deployment import deployment_system_prompt
from src.sdlccopilot.logger import logging
from src.sdlccopilot.exception import CustomException
import sys

class DeploymentHelper:
    def __init__(self, llm):
        self.llm = llm
        
    def generate_deployment_steps_with_llm(self, frontend_code, backend_code):
        try:
            logging.info("Generating deployment steps with LLM...")
            user_query =  f"Create a deployment steps for the this frontend code: {frontend_code} and backend code: {backend_code}"
            chain = prompt_template | self.llm 
            response = chain.invoke({"system_prompt" : deployment_system_prompt, "human_query" : user_query})
            logging.info("Deployment steps generated with LLM.")
            logging.info(f"In generate_deployment_steps_with_llm : {response}")
            return response.content
        except Exception as e:
            logging.error(f"Error generating deployment steps: {str(e)}")
            raise CustomException(e, sys)