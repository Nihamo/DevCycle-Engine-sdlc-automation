from typing import Literal
from langchain_core.messages import AIMessage
from src.sdlccopilot.helpers.code import CodeHelper
from src.sdlccopilot.logger import logging
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.utils.constants import CONSTANT_FRONTEND_CODE, CONSTANT_REVISED_FRONTEND_CODE, CONSTANT_BACKEND_CODE, CONSTANT_REVISED_BACKEND_CODE
import os
import time
class DevelopmentNodes:
    def __init__(self, llm): 
        self.code_helper = CodeHelper(llm)
    
    ## Frontend Code Development Nodes
    def generate_frontend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In generate_frontend_code...")
        frontend_code = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            functional_doc = getattr(state, 'functional_documents', None) or ''
            technical_doc = getattr(state, 'technical_documents', None) or ''
            frontend_code = self.code_helper.generate_frontend_code_from_llm(
                state.user_stories,
                functional_document=functional_doc,
                technical_document=technical_doc
            )
        else:
            time.sleep(10)
            frontend_code = CONSTANT_FRONTEND_CODE
        code_type = "frontend"
        logging.info(f"Generated frontend code")
        return {
            f"{code_type}_code" : frontend_code,
            f"{code_type}_status": 'pending_approval',
            f"{code_type}_messages": AIMessage(
                content=f"Please review {code_type} design document and provide feedback or type 'Approved' if you're satisfied."
            ),
        }

    def review_frontend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In review_frontend_code")
        user_feedback = state.frontend_messages[-1].content.lower().strip()
        logging.info(f"User feedback: {user_feedback}")
        approved = user_feedback == "approved"
        code_type = "frontend"
        return {
            f"{code_type}_messages":AIMessage(
                content="Great! Code have been finalized. You can now proceed with next steps."
                if approved else
                "I've received your feedback. I'll revise the design documents accordingly."),
            f"{code_type}_status": "approved" if approved else "feedback"
        }

    def should_fix_frontend_code(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.frontend_status == 'approved' else 'feedback'

    def fix_frontend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In fix_frontend_code...")
        code_type = "frontend"
        user_feedback = state.frontend_messages[-2].content.lower().strip()
        revised_count = state.revised_count + 1
        logging.info(f"revised_count : {revised_count}")

        if revised_count == 3:
            return {
                f"{code_type}_messages": AIMessage(
                    content="Code have been revision maxed out. Please review the code and continue with the next step."
                ),
                f"{code_type}_status": "approved"
            }
        
        revised_code = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            revised_code = self.code_helper.revised_frontend_code_from_llm(state.frontend_code, user_feedback)
        else:
            time.sleep(10)
            revised_code = CONSTANT_REVISED_FRONTEND_CODE
        return {
            f"{code_type}_code": revised_code,
            f"{code_type}_messages": AIMessage(
                content=f"Please review revised {code_type} code and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            f"{code_type}_status": "pending_approval",
            "revised_count": revised_count
        }
    
    def generate_backend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In generate_backend_code...")
        backend_code = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            functional_doc = getattr(state, 'functional_documents', None) or ''
            technical_doc = getattr(state, 'technical_documents', None) or ''
            backend_code = self.code_helper.generate_backend_code_from_llm(
                state.user_stories,
                functional_document=functional_doc,
                technical_document=technical_doc
            )
        else:
            time.sleep(10)
            backend_code = CONSTANT_BACKEND_CODE
        code_type = "backend"
        logging.info(f"Generated backend code")
        return {
            f"{code_type}_code" : backend_code,
            f"{code_type}_status": 'pending_approval',
            f"{code_type}_messages": AIMessage(
                content=f"Please review {code_type} design document and provide feedback or type 'Approved' if you're satisfied."
            ),
        }

    def review_backend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In review_backend_code")
        user_feedback = state.backend_messages[-1].content.lower().strip()
        logging.info(f"User feedback: {user_feedback}")
        approved = user_feedback == "approved"
        code_type = "backend"
        return {
            f"{code_type}_messages":AIMessage(
                content="Great! Code have been finalized. You can now proceed with next steps."
                if approved else
                "I've received your feedback. I'll revise the design documents accordingly."),
            f"{code_type}_status": "approved" if approved else "feedback"
        }

    def should_fix_backend_code(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.backend_status == 'approved' else 'feedback'

    def fix_backend_code(self, state : SDLCState) -> SDLCState:
        logging.info("In fix_backend_code...")
        code_type = "backend"
        user_feedback = state.backend_messages[-2].content.lower().strip()
        revised_count = state.revised_count + 1
        logging.info(f"revised_count : {revised_count}")

        if revised_count == 3:
            return {
                f"{code_type}_messages": AIMessage(
                    content="Code have been revision maxed out. Please review the code and continue with the next step."
                ),
                f"{code_type}_status": "approved"
            }
        
        revised_code = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            revised_code = self.code_helper.revised_backend_code_from_llm(state.backend_code, user_feedback)
        else:
            time.sleep(10)
            revised_code = CONSTANT_REVISED_BACKEND_CODE
        return {
            f"{code_type}_code": revised_code,
            f"{code_type}_messages": AIMessage(
                content=f"Please review revised {code_type} code and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            f"{code_type}_status": "pending_approval",
            "revised_count": revised_count
        }
        