
from langchain_core.messages import AIMessage
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.security_review import SecurityReviewHelper
from typing_extensions import Literal
import os
from src.sdlccopilot.utils.constants import CONSTANT_SECURITY_REVIEW, CONSTANT_REVISED_BACKEND_CODE
import time
class SecurityReviewNodes:
    def __init__(self, gemini_llm, anthropic_llm): 
        self.security_review_helper = SecurityReviewHelper(gemini_llm, anthropic_llm)
        
    def generate_security_reviews(self, state : SDLCState) -> SDLCState:
        logging.info("In generate_security_reviews...")
        security_reviews = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            security_reviews = self.security_review_helper.generate_security_reviews_from_llm(state.backend_code)
        else:
            time.sleep(10)
            security_reviews = CONSTANT_SECURITY_REVIEW
        logging.info("Security reviews generated successfully !!!")
        return {
            "security_reviews": security_reviews,
            "security_reviews_status": "pending_approval",
            "security_reviews_messages": AIMessage(
                content=f"Please review security reviews and provide feedback or type 'Approved' if you're satisfied."
            ),
        }

    def security_review(self, state : SDLCState) -> SDLCState:
        logging.info("In security_review...")
        user_feedback = state.security_reviews_messages[-1].content.lower().strip()
        logging.info(f"user feedback: {user_feedback}")
        approved = user_feedback == "approved"
        return {
            "security_reviews_status": "approved" if approved else "feedback",
            "security_reviews_messages": AIMessage(
                content="Great! Security reviews have been finalized. You can now proceed with next steps."
                if approved else
                "I've received your feedback. I'll revise the security reviews accordingly."),
        }

    def should_fix_code_after_security_review(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.security_reviews_status == 'approved' else 'feedback'

    def fix_code_after_security_review(self, state : SDLCState) -> SDLCState:
        logging.info("In fix_code_after_security_review...")
        code_type = "backend"
        user_feedback = state.security_reviews_messages[-2].content.lower().strip()
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
            revised_code = self.security_review_helper.revised_backend_code_with_security_reviews_from_llm(state.backend_code, state.security_reviews, user_feedback)
        else:
            time.sleep(10)
            revised_code = CONSTANT_REVISED_BACKEND_CODE
        logging.info("Backend code revised according to security reviews with LLM !!!")
        return {
            f"{code_type}_code": revised_code,
            f"{code_type}_messages": AIMessage(
                content=f"Please review revised {code_type} code and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            f"{code_type}_status": "pending_approval",
            "revised_count": revised_count
        }