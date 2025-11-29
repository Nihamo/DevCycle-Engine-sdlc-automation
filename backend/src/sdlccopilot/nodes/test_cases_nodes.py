

from langchain_core.messages import AIMessage
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.test_case import TestCaseHelper
from typing_extensions import Literal
import os
from src.sdlccopilot.utils.constants import CONSTANT_TEST_CASES, CONSTANT_REVISED_TEST_CASES
import time
class TestCaseNodes:
    def __init__(self, llm): 
        self.test_case_helper = TestCaseHelper(llm)

    def generate_test_cases(self, state : SDLCState) -> SDLCState: 
        logging.info("In generate_test_cases...")  
        test_cases = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            test_cases = self.test_case_helper.generate_test_cases_from_llm(state.functional_documents)
        else:
            time.sleep(10)
            test_cases = CONSTANT_TEST_CASES
        logging.info("Test cases generated successfully !!!")
        return {
            "test_cases": test_cases,
            "test_cases_status": "pending_approval",
            "test_cases_messages": AIMessage(
                content=f"Please review test cases and provide feedback or type 'Approved' if you're satisfied."
            ),
        }

    def test_cases_review(self, state : SDLCState) -> SDLCState:
        logging.info("In test_cases_review...")
        user_feedback = state.test_cases_messages[-1].content.lower().strip()
        logging.info(f"user feedback: {user_feedback}")
        approved = user_feedback == "approved"
        return {
            "test_cases_status": "approved" if approved else "feedback",
            "test_cases_messages": AIMessage(
                content="Great! Test cases have been finalized. You can now proceed with next steps."
                if approved else
                "I've received your feedback. I'll revise the test cases accordingly."),
        }

    def should_fix_test_cases(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.test_cases_status == 'approved' else 'feedback'

    def revised_test_cases(self, state : SDLCState) -> SDLCState:
        logging.info("In revised_test_cases...")
        user_feedback = state.test_cases_messages[-2].content.lower().strip()
        revised_count = state.revised_count + 1
        logging.info(f"revised_count : {revised_count}")
        if revised_count == 50:
            logging.info("Test cases revision maxed out !!!")
            return {
                "test_cases_messages": AIMessage(
                    content="Test cases have been revision maxed out. Please review the test cases and continue with the next step."
                ),
                "test_cases_status": "approved"
            }
        test_cases = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            test_cases = self.test_case_helper.revised_test_cases_from_llm(state.test_cases, user_feedback)
        else:
            time.sleep(10)
            test_cases = CONSTANT_REVISED_TEST_CASES
        return {
            "test_cases": test_cases,
            "test_cases_messages": AIMessage(
                content=f"Please review revised test cases and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            "test_cases_status": "pending_approval",
            "revised_count": revised_count
    }
