from langchain_core.messages import AIMessage
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.deployment import DeploymentHelper
from src.sdlccopilot.utils.constants import CONSTANT_DEPLOYMENT_STEPS
import os
import time

class DeploymentNodes:
    def __init__(self, llm): 
        self.deployment_helper = DeploymentHelper(llm)
        
    def generate_deployment_steps(self, state : SDLCState) -> SDLCState:
        logging.info("In generate_deployment_steps...")
        frontend_code = state.frontend_code
        backend_code = state.backend_code
        deployment_steps = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            deployment_steps = self.deployment_helper.generate_deployment_steps_with_llm(frontend_code, backend_code)
        else:
            time.sleep(10)
            deployment_steps = CONSTANT_DEPLOYMENT_STEPS
        logging.info("Deployment steps generated successfully !!!")
        return {
            "deployment_steps" : deployment_steps,
            "deployment_status" : "approved",
            "deployment_messages" : AIMessage(content="Please follow these steps to deploy the code.")
        }