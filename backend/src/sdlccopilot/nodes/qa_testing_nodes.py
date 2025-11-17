
from langchain_core.messages import AIMessage
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.qa_testing import QATestingHelper
from typing_extensions import Literal
from src.sdlccopilot.utils.constants import CONSTANT_QA_TESTING_RESULTS, CONSTANT_REVISED_BACKEND_CODE
import os
from src.sdlccopilot.logger import logging
import time
CONSTANT_TEST_CASES = [
  {
    "test_id": "TC001",
    "description": "Enable MFA with valid userId and mfaType",
    "steps": [
      "Send POST request to /api/auth/mfa/enable",
      "Include JSON body with userId: 'user123' and mfaType: 'mpin'",
      "Expect response status 200 and message 'MFA enabled successfully'"
    ],
    "status": "draft"
  },
  {
    "test_id": "TC002",
    "description": "Apply for a loan with valid amount and term",
    "steps": [
      "Send POST request to /api/loan/apply",
      "Include JSON body with amount: 50000 and term: 12",
      "Expect response with loanId, status: 'PENDING', and interest value"
    ],
    "status": "draft"
  },
  {
    "test_id": "TC003",
    "description": "Link a bank account with valid details",
    "steps": [
      "Send POST request to /api/bank/link",
      "Include JSON body with accountNumber: '1234567890' and bankName: 'BankX'",
      "Expect response status 200 and message 'Bank account linked successfully'"
    ],
    "status": "draft"
  },
  {
    "test_id": "TC004",
    "description": "Pay a bill with valid billId and amount",
    "steps": [
      "Send POST request to /api/bill/pay",
      "Include JSON body with billId: 'bill123' and amount: 1500",
      "Expect response with transactionId and status: 'SUCCESS'"
    ],
    "status": "draft"
  },
  {
    "test_id": "TC005",
    "description": "Purchase an insurance policy with valid policyId and term",
    "steps": [
      "Send POST request to /api/insurance/purchase",
      "Include JSON body with policyId: 'pol789' and term: 5",
      "Expect response with policyNumber, status: 'ACTIVE', and coverage amount"
    ],
    "status": "draft"
  }
]

class QATestingNodes:
    def __init__(self, gemini_llm, anthropic_llm): 
        self.qa_testing_helper = QATestingHelper(gemini_llm, anthropic_llm)
        
    def perform_qa_testing(self, state : SDLCState) -> SDLCState:
        logging.info("In perform_qa_testing...")
        test_cases = CONSTANT_TEST_CASES
        # TODO : get test cases from the state
        # test_cases = state.test_cases
        qa_testing = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":  
            qa_testing = self.qa_testing_helper.perform_qa_testing_with_llm(test_cases, state.backend_code)
        else:
            time.sleep(10)
            qa_testing = CONSTANT_QA_TESTING_RESULTS
        
        if qa_testing['summary']['pass_percentage'] > 50:
            logging.info("QA testing passed.")
            return {
                "qa_testing": qa_testing,
                "qa_testing_status": "passed",
                "qa_testing_messages": AIMessage(
                  content="Great! QA testing have been finalized. You can now proceed with next steps."
                )
            }
        else:
            logging.info("QA testing failed.")
            return {
                "qa_testing": qa_testing,
                "qa_testing_status": "failed",
                "qa_testing_messages": AIMessage(
                  content="QA testing have been failed. I've revised the code according to the QA testing results."
                )
            }

    def should_fix_code_after_qa_testing(self, state : SDLCState) -> Literal["passed", "failed"]:
        return "passed" if state.qa_testing_status == 'passed' else 'failed'

    def fix_code_after_qa_testing(self, state : SDLCState) -> SDLCState:
        logging.info("In fix_code_after_qa_testing...")
        code_type = "backend"
        revised_count = state.revised_count + 1
        logging.info(f"revised_count : {revised_count}")

        if revised_count == 3:
            return {
                f"{code_type}_messages": AIMessage(
                    content="Code have been revision maxed out. Please review the code and continue with the next step."
                ),
                f"{code_type}_status": "approved"
            }
        
        failed_test_cases = [test_case for test_case in state.qa_testing if test_case['status'] == "failed"]
        revised_code = None
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            revised_code = self.qa_testing_helper.revised_backend_code_with_qa_testing_from_llm(state.backend_code, failed_test_cases)
        else:
            time.sleep(10)
            revised_code = CONSTANT_REVISED_BACKEND_CODE
        logging.info("Fixed code after QA testing completed !!!")
        return {
            f"{code_type}_code": revised_code,
            f"{code_type}_messages": AIMessage(
                content=f"Please review revised {code_type} code and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            f"{code_type}_status": "pending_approval",
            "revised_count": revised_count
        }