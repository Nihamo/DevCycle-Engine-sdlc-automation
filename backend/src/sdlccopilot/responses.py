from pydantic import BaseModel, Field
from typing import List, Dict, Literal
from src.sdlccopilot.states.qa import QATesting

class UserStoriesResponse(BaseModel):
    session_id: str = Field(description="The session id")
    status: Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the user stories")
    project_requirements : Dict = Field(description="The project requirements")
    user_stories: List[Dict] = Field(description="The user stories")
    message: List[Dict] = Field(description="The messages")


class DocumentSection(BaseModel):
    title: str = Field(description="The title of the section") 
    content: str = Field(description="The content of the section")

class DesignDocumentsResponse(BaseModel):
    session_id: str = Field(description="The session id")
    document_type: Literal["functional", "technical"] = Field(description="The type of the document")
    status: Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the document")
    document : str = Field(description="The document")
    messages: List[Dict] = Field(description="The messages")
   
class CodeResponse(BaseModel):
    session_id : str = Field(description="The session id")
    code_type : Literal["frontend", "backend"] = Field(description="The type of the code")
    status : Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the code")
    code : str = Field(description="The code")
    messages : List[Dict] = Field(description="The messages")


class SecurityReview(BaseModel):
    sec_id : str = Field(description="The id of the security review")
    review : str = Field(description="The review of the security review")
    file_path : str = Field(description="The file path of the security review")
    recommendation : str = Field(description="The recommendation of the security review")
    priority : Literal["high", "medium", "low"] = Field(description="The priority of the security review")
    
class SecurityReviewResponse(BaseModel):
    session_id : str = Field(description="The session id")
    status : Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the security review")
    reviews : List[SecurityReview] = Field(description="The reviews")
    messages : List[Dict] = Field(description="The messages")


class TestCase(BaseModel):
    test_id : str = Field(description="The test id")
    description : str = Field(description="The description")
    steps : List[str] = Field(description="The steps")
    status : Literal["draft", "pass", "fail"] = Field(default="draft", description="The status")
    
    
class TestCasesResponse(BaseModel):
    session_id : str = Field(description="The session id")
    status : Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the test cases")
    test_cases : List[TestCase] = Field(description="The test cases")
    messages : List[Dict] = Field(description="The messages")
    
class QATestingResponse(BaseModel):
    session_id : str = Field(description="The session id")
    status : Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the qa testing")
    qa_testing : QATesting = Field(description="The qa testing")
    messages : List[Dict] = Field(description="The messages")
    
class DeploymentResponse(BaseModel):
    session_id : str = Field(description="The session id")
    status : Literal["in_progress", "pending_approval", "feedback", "completed"] = Field(description="The status of the deployment")
    deployment_steps : str = Field(description="The deployment steps")
    messages : List[Dict] = Field(description="The messages")

#     ********* document_state :  {'functional_documents': [DocumentSection(title='INTRODUCTION', content='This document defines the functional requirements for the Password Reset 
# Feature of the User Management System.'), DocumentSection(title='BUSINESS CONTEXT', content='The business needs a secure mechanism for users to recover access to their accounts without compromising security, improving customer satisfaction and retention.')], 'technical_documents': [], 'messages': [AIMessage(content="Please review above functional design document and provide feedback or type 'Approved' if you're satisfied.", additional_kwargs={}, response_metadata={}, id='41a4334f-abcd-4e48-a1ce-f96f36454b07')], 'document_type': 'functional', 'status': 'pending_approval', 'revised_count': 0, 'version': 1.0}