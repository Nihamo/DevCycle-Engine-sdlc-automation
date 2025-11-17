from typing_extensions import Annotated, List, Literal
from src.sdlccopilot.states.story import UserStory, ProjectRequirements
from src.sdlccopilot.states.security import SecurityReview
from src.sdlccopilot.states.testcase import TestCase
from src.sdlccopilot.states.qa import QATesting, TestSummary
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class SDLCState(BaseModel):
    project_requirements : ProjectRequirements
    revised_count : int = Field(default=0, description="The number of times the revised")
    # User story
    user_stories : List[UserStory] = []
    user_story_messages : Annotated[list, add_messages] = []
    user_story_status : Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"
    
    # functional documents
    functional_documents : str = Field(default='', description='The functional documents')
    functional_messages : Annotated[list, add_messages] = []
    functional_status: Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"
    
    # technical documents
    technical_documents : str = Field(default='', description='The technical documents')
    technical_messages : Annotated[list, add_messages] = []
    technical_status: Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"
    
    # frontend code
    frontend_code : str = Field(default='', description="The frontend code")
    frontend_messages: Annotated[list, add_messages] = []
    frontend_status: Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"
    
    # backend code
    backend_code : str = Field(default= '', description="The backend code")
    backend_messages: Annotated[list, add_messages] = []
    backend_status: Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"

    # security review
    security_reviews : List[SecurityReview] = []
    security_reviews_messages: Annotated[list, add_messages] = []
    security_reviews_status : Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"

    ## test cases
    test_cases : List[TestCase] = []
    test_cases_messages: Annotated[list, add_messages] = []
    test_cases_status : Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"

    ## qa testing
    qa_testing : QATesting = Field(default=QATesting(test_results=[], summary=TestSummary(total_tests=0, passed=0, failed=0, pass_percentage=0.0)), description="The qa testing results")
    qa_testing_messages: Annotated[list, add_messages] = []
    qa_testing_status : Literal["pending", "passed", "failed"] = "pending"

    ## Code deployment
    deployment_steps : str = Field(default='', description="The code deployment steps")
    deployment_messages: Annotated[list, add_messages] = [] 
    deployment_status : Literal["pending", "in_progress", "pending_approval", "feedback", "approved"] = "pending"


