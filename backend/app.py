from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from uuid import uuid4
from src.sdlccopilot.requests import ProjectRequirementsRequest, OwnerFeedbackRequest
from src.sdlccopilot.responses import UserStoriesResponse, DesignDocumentsResponse, CodeResponse, SecurityReviewResponse, SecurityReview, TestCasesResponse, QATestingResponse, DeploymentResponse
from src.sdlccopilot.graph.sdlc_graph import SDLCGraphBuilder
from src.sdlccopilot.logger import logging
from redis import Redis
import os 
import httpx
import json
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
import time

from dotenv import load_dotenv
load_dotenv()
## Environment Variable
os.environ['PROJECT_ENVIRONMENT'] = os.getenv("PROJECT_ENVIRONMENT")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGSMITH_PROJECT'] = os.getenv("LANGSMITH_PROJECT")
os.environ['LANGSMITH_TRACING'] = os.getenv("LANGSMITH_TRACING")
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Application state management
class ApplicationState:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        self.sdlc_workflow = None

    async def initialize(self):
        self.redis = Redis(
            host= REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            username="default",
            password=REDIS_PASSWORD
        )
        self.http_client = httpx.AsyncClient()
        sdlc_graph_builder = SDLCGraphBuilder()
        self.sdlc_workflow = sdlc_graph_builder.build()

    async def shutdown(self):
        if self.http_client:
            await self.http_client.aclose()
        if self.redis:
            self.redis.close()

app = FastAPI(
    title="SDLC Copilot API",
    description="API for managing the Software Development Life Cycle process",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    app.state.app_state = ApplicationState()
    await app.state.app_state.initialize()
    
    
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.app_state.shutdown()
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
async def get_redis() -> Redis:
    return app.state.app_state.redis

async def get_http_client() -> httpx.AsyncClient:
    return app.state.app_state.http_client

async def get_sdlc_workflow():
    return app.state.app_state.sdlc_workflow

# Helper functions
def serialize_message(msg) -> Dict[str, Any]:
    return {
        "content": msg.content,
        "type": msg.type,
        "id": msg.id
    }


# Status response model
class ServerStatusResponse(BaseModel):
    status: str
    message: str

# Error handling
class SDLCException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        logging.error(f"SDLC Error: {detail}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/status", response_model=ServerStatusResponse)
async def get_server_status():
    return ServerStatusResponse(
        status="OK",
        message="Server is up and running..."
    )

@app.post("/stories/generate", response_model=UserStoriesResponse)
async def generate_user_stories(
    request: ProjectRequirementsRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Generating user stories for project: {request.title}")
    session_id = str(uuid4())
    
    try:
        project_requirements = {
            "title": request.title,
            "description": request.description,
            "requirements": request.requirements
        }

        initial_story_state = {
            "project_requirements": project_requirements,
            "user_stories": [],
            "user_stories_messages": HumanMessage(content=f"{project_requirements}"),
            "status": "in_progress",
            "owner_feedback": "",
            "review_count": 0
        }

        state = None
        thread = {"configurable": {"thread_id": session_id}}
        for event in sdlc_workflow.stream(initial_story_state, thread, stream_mode="values"):
            state = event

        user_story_status = "completed" if state["user_story_status"] == 'approved' else state["user_story_status"]
        user_story = state["user_stories"]
        user_story_messages = [serialize_message(msg) for msg in state["user_story_messages"]]

        session_data = {
            "project_requirements": project_requirements,
            "user_stories": user_story,
            "user_story_status": user_story_status,
            "user_story_messages": user_story_messages
        }
                
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"User stories generated successfully for session: {session_id}")

        return UserStoriesResponse(
            session_id=session_id,
            project_requirements=project_requirements,
            status=user_story_status,
            user_stories=user_story,
            message=user_story_messages
        )    

    except Exception as e:
        logging.error(f"Error generating user stories: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

@app.post("/stories/review/{session_id}", response_model=UserStoriesResponse)
async def review_user_stories(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing user stories for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "user_story_review")
    
    try:
        thread = {"configurable": {"thread_id": session_id}}
        sdlc_state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {sdlc_state.next}")

        sdlc_workflow.update_state(thread, {"user_story_messages": HumanMessage(content=feedback)})

        sdlc_state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            sdlc_state = event
            
        logging.debug(f"Updated state: {sdlc_state}")
        user_story_status = "completed" if sdlc_state["user_story_status"] == 'approved' else sdlc_state["user_story_status"]
        user_story = sdlc_state["user_stories"]
        user_story_messages = [serialize_message(msg) for msg in sdlc_state["user_story_messages"]]
        
        logging.debug(f"User story status: {user_story_status}")
        
        if user_story_status == "completed":
            functional_documents = sdlc_state["functional_documents"]
            functional_status = sdlc_state["functional_status"]
            functional_messages = [serialize_message(msg) for msg in sdlc_state["functional_messages"]]

        session_data = {
            **session_data,
            "user_stories": user_story,
            "user_story_status": user_story_status,
            "user_story_messages": user_story_messages,
            "functional_documents": functional_documents if user_story_status == "completed" else None,
            "functional_status": functional_status if user_story_status == "completed" else None,
            "functional_messages": functional_messages if user_story_status == "completed" else None
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"User stories reviewed successfully for session: {session_id}")

        return UserStoriesResponse(
            session_id=session_id,
            project_requirements=session_data["project_requirements"],
            status=user_story_status,
            user_stories=user_story,
            message=user_story_messages
        )    

    except Exception as e:
        logging.error(f"Error reviewing user stories: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))


@app.post("/documents/functional/generate/{session_id}", response_model=DesignDocumentsResponse)
async def create_functional_design_documents(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Generating functional design documents for session: {session_id}")
    session_data = session_validator(session_id, redis, "functional_generate")
    try:
        functional_status = session_data["functional_status"]
        functional_documents = session_data["functional_documents"]
        functional_messages = session_data["functional_messages"]

        logging.info(f"Functional documents generated successfully for session: {session_id}")

        return DesignDocumentsResponse.model_construct(
            session_id=session_id,
            document_type="functional",
            status=functional_status,
            document=functional_documents,
            messages=functional_messages
        )

    except Exception as e:
        logging.error(f"Error generating functional documents: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))


@app.post("/documents/functional/review/{session_id}", response_model=DesignDocumentsResponse)
async def review_functional_design_documents(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing functional design documents for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "functional_review")
    try:
        thread = {"configurable": {"thread_id": session_id}}
        sdlc_state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {sdlc_state.next}")
        
        sdlc_workflow.update_state(thread, {"functional_messages": HumanMessage(content=feedback)})
        sdlc_state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            sdlc_state = event
            
        logging.debug(f"Functional document state: {sdlc_state}")
        
        functional_status = "completed" if sdlc_state["functional_status"] == 'approved' else sdlc_state["functional_status"]
        functional_messages = [serialize_message(msg) for msg in sdlc_state["functional_messages"]]

        if functional_status == "completed":
            technical_documents = sdlc_state["technical_documents"]
            technical_status = sdlc_state["technical_status"]
            technical_messages = [serialize_message(msg) for msg in sdlc_state["technical_messages"]]
            
        session_data = {
            **session_data,
            "functional_documents": sdlc_state["functional_documents"],
            "functional_messages": functional_messages,
            "functional_status": functional_status,
            "technical_documents": technical_documents if functional_status == "completed" else None,
            "technical_messages": technical_messages if functional_status == "completed" else None,
            "technical_status": technical_status if functional_status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Functional documents reviewed successfully for session: {session_id}")

        return DesignDocumentsResponse.model_construct(
            session_id=session_id,
            document_type="functional",
            status=functional_status,
            document=sdlc_state["functional_documents"],
            messages=functional_messages
        )

    except Exception as e:
        logging.error(f"Error reviewing functional documents: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))
    

@app.post("/documents/technical/generate/{session_id}", response_model=DesignDocumentsResponse)
async def create_technical_design_documents(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Generating technical design documents for session: {session_id}")
    session_data = session_validator(session_id, redis, "technical_generate")
    
    try:
        technical_status = session_data["technical_status"]
        technical_documents = session_data["technical_documents"]
        technical_messages = session_data["technical_messages"]
        
        logging.info(f"Technical documents generated successfully for session: {session_id}")
        
        return DesignDocumentsResponse.model_construct(
            session_id=session_id,
            document_type="technical",
            status=technical_status,
            document=technical_documents,
            messages=technical_messages
        )

    except Exception as e:
        logging.error(f"Error generating technical documents: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

@app.post("/documents/technical/review/{session_id}", response_model=DesignDocumentsResponse)
async def review_technical_design_documents(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing technical design documents for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "technical_review")
    
    try:
        
        thread = {"configurable": {"thread_id": session_id}}
        sdlc_state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {sdlc_state.next}")

        sdlc_workflow.update_state(thread, {"technical_messages": HumanMessage(content=feedback)})

        sdlc_state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            sdlc_state = event
            
        logging.debug(f"Technical document state: {sdlc_state}")
                
        technical_status = "completed" if sdlc_state["technical_status"] == 'approved' else sdlc_state["technical_status"]
        technical_messages = [serialize_message(msg) for msg in sdlc_state["technical_messages"]]
        
        if technical_status == "completed":
            frontend_documents = sdlc_state["frontend_code"]
            frontend_status = sdlc_state["frontend_status"]
            frontend_messages = [serialize_message(msg) for msg in sdlc_state["frontend_messages"]]

        session_data = {
            **session_data,
            "technical_documents": sdlc_state["technical_documents"],
            "technical_messages": technical_messages,
            "technical_status": technical_status,
            "frontend_code": frontend_documents if technical_status == "completed" else None,
            "frontend_messages": frontend_messages if technical_status == "completed" else None,
            "frontend_status": frontend_status if technical_status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Technical documents reviewed successfully for session: {session_id}")

        return DesignDocumentsResponse.model_construct(
            session_id=session_id,
            document_type="technical",
            status=technical_status,
            document=sdlc_state["technical_documents"],
            messages=technical_messages
        )

    except Exception as e:
        logging.error(f"Error reviewing technical documents: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

## Frontend code
@app.post("/code/frontend/generate/{session_id}", response_model=CodeResponse)
async def generate_frontend_code(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Generating frontend code for session: {session_id}")
    session_data = session_validator(session_id, redis, "frontend_generate")
    
    try:
        frontend_status = session_data["frontend_status"]
        frontend_code = session_data["frontend_code"]
        frontend_messages = session_data["frontend_messages"]
        
        logging.info(f"Frontend code generated successfully for session: {session_id}")

        return CodeResponse.model_construct(
            session_id=session_id,
            code_type="frontend",
            status=frontend_status,
            code=frontend_code,
            messages=frontend_messages,
        )
    
    except Exception as e:
        logging.error(f"Error generating frontend code: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))
    
@app.post("/code/frontend/review/{session_id}", response_model=CodeResponse)
async def review_frontend_code(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing frontend code for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "frontend_review")
    
    try:
        thread = {"configurable": {"thread_id": session_id}}
        sdlc_state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {sdlc_state.next}")

        sdlc_workflow.update_state(thread, {"frontend_messages": HumanMessage(content=feedback)})

        sdlc_state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            sdlc_state = event
            
        logging.debug(f"Frontend code state: {sdlc_state}")
        
        frontend_status = "completed" if sdlc_state["frontend_status"] == 'approved' else sdlc_state["frontend_status"]
        frontend_messages = [serialize_message(msg) for msg in sdlc_state["frontend_messages"]]
        
        if frontend_status == "completed":
            backend_code = sdlc_state["backend_code"]
            backend_status = sdlc_state["backend_status"]
            backend_messages = [serialize_message(msg) for msg in sdlc_state["backend_messages"]]
        
        session_data = {
            **session_data,    
            "frontend_code": sdlc_state["frontend_code"],
            "frontend_messages": frontend_messages,
            "frontend_status": frontend_status,
            "backend_code": backend_code if frontend_status == "completed" else None,
            "backend_messages": backend_messages if frontend_status == "completed" else None,
            "backend_status": backend_status if frontend_status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Frontend code reviewed successfully for session: {session_id}")
        
        return CodeResponse.model_construct(
            session_id=session_id,
            code_type="frontend",
            status=frontend_status,
            code=sdlc_state["frontend_code"],
            messages=frontend_messages,
        )

    except Exception as e:
        logging.error(f"Error reviewing frontend code: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

# Backend code endpoints
@app.post("/code/backend/generate/{session_id}", response_model=CodeResponse)
async def generate_backend_code(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Generating backend code for session: {session_id}")
    session_data = session_validator(session_id, redis, "backend_generate")
    
    try:
        backend_status = session_data["backend_status"]
        backend_status = session_data["backend_status"]
        backend_code = session_data["backend_code"]
        backend_messages = session_data["backend_messages"]
        logging.info(f"Backend code generated successfully for session: {session_id}")
        return CodeResponse.model_construct(
            session_id=session_id,
            code_type="backend",
            status=backend_status,
            code=backend_code,
            messages=backend_messages,
        )
    
    except Exception as e:
        logging.error(f"Error generating backend code: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

@app.post("/code/backend/review/{session_id}", response_model=CodeResponse)
async def review_backend_code(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing backend code for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "backend_review")
    
    try:
        thread = {"configurable": {"thread_id": session_id}}
        document_state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {document_state.next}")
        
        sdlc_workflow.update_state(thread, {"backend_messages": HumanMessage(content=feedback)})

        state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            state = event
        
        logging.debug(f"Updated state: {state}")
        status = "completed" if state["backend_status"] == 'approved' else state["backend_status"]
        
        backend_messages = [serialize_message(msg) for msg in state["backend_messages"]]
        if status == "completed":
            security_reviews = state["security_reviews"]
            security_reviews_status = state["security_reviews_status"]
            security_reviews_messages = [serialize_message(msg) for msg in state["security_reviews_messages"]]
            
        session_data = {
            **session_data,    
            "backend_code": state["backend_code"],
            "backend_messages": backend_messages,
            "backend_status": status,
            "security_reviews": security_reviews if status == "completed" else None,
            "security_reviews_messages": security_reviews_messages if status == "completed" else None,
            "security_reviews_status": security_reviews_status if status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Backend code reviewed successfully for session: {session_id}")
        
        return CodeResponse.model_construct(
            session_id=session_id,
            code_type="backend",
            status=status,
            code=state["backend_code"],
            messages=backend_messages,
        )

    except Exception as e:
        logging.error(f"Error reviewing backend code: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

# Security review endpoints
@app.get("/security/review/get/{session_id}", response_model=SecurityReviewResponse)
async def get_security_review(
    session_id: str,
    redis: Redis = Depends(get_redis),
):
    logging.info(f"Getting security review for session: {session_id}")
    session_data = session_validator(session_id, redis, "security_review")
    try:
        reviews = session_data["security_reviews"]
        status = session_data["security_reviews_status"]
        messages = session_data["security_reviews_messages"]
        logging.info(f"Security review retrieved successfully for session: {session_id}")
        
        return SecurityReviewResponse.model_construct(
            session_id=session_id,
            status=status,
            reviews=reviews,
            messages=messages
        )
        
    except Exception as e:
        logging.error(f"Error getting security review: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

@app.post("/security/review/review/{session_id}", response_model=SecurityReviewResponse)
async def review_security_review(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing security review for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "security_review")
    
    try:
        thread = {"configurable": {"thread_id": session_id}}
        state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {state.next}")
        
        sdlc_workflow.update_state(thread, {"security_reviews_messages": HumanMessage(content=feedback)})

        state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            state = event
        
        logging.debug(f"Updated state: {state}")
        status = "completed" if state["security_reviews_status"] == 'approved' else state["security_reviews_status"]
        security_reviews_messages = [serialize_message(msg) for msg in state["security_reviews_messages"]]
        
        # Initialize variables to avoid NameError
        test_cases = None
        test_cases_status = None
        test_cases_messages = None
        
        if status == "completed":
            test_cases = state.get("test_cases")
            test_cases_status = state.get("test_cases_status")
            test_cases_messages = [serialize_message(msg) for msg in state.get("test_cases_messages", [])]
            
        session_data = {
            **session_data,    
            "security_reviews": state.get("security_reviews", []),
            "security_reviews_messages": security_reviews_messages,
            "security_reviews_status": status,
            "test_cases": test_cases if status == "completed" else None,
            "test_cases_messages": test_cases_messages if status == "completed" else None,
            "test_cases_status": test_cases_status if status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Security review reviewed successfully for session: {session_id}")

        # Ensure security_reviews is a list, not a tuple
        security_reviews = state.get("security_reviews", [])
        if isinstance(security_reviews, tuple):
            security_reviews = list(security_reviews)
        
        return SecurityReviewResponse.model_construct(
            session_id=session_id,
            status=status,
            reviews=security_reviews,
            messages=security_reviews_messages
        )

    except Exception as e:
        logging.error(f"Error reviewing security review: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

# Test cases endpoints
@app.get("/test/cases/get/{session_id}", response_model=TestCasesResponse)
async def get_test_cases(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Getting test cases for session: {session_id}")
    session_data = session_validator(session_id, redis, "test_cases_generate")
    
    try:
        test_cases = session_data["test_cases"]
        status = session_data["test_cases_status"]
        messages = session_data["test_cases_messages"]
        logging.info(f"Test cases retrieved successfully for session: {session_id}")
        return TestCasesResponse.model_construct(
            session_id=session_id,
            status=status,
            test_cases=test_cases,
            messages=messages
        )
        
    except Exception as e:
        logging.error(f"Error getting test cases: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

@app.post("/test/cases/review/{session_id}", response_model=TestCasesResponse)
async def review_test_cases(
    session_id: str,
    request: OwnerFeedbackRequest,
    redis: Redis = Depends(get_redis),
    sdlc_workflow = Depends(get_sdlc_workflow)
):
    logging.info(f"Reviewing test cases for session: {session_id}")
    feedback = request.feedback
    session_data = session_validator(session_id, redis, "test_cases_review")
    
    try:
        thread = {"configurable": {"thread_id": session_id}}
        state = sdlc_workflow.get_state(thread)
        logging.debug(f"Next node to call: {state.next}")
        
        sdlc_workflow.update_state(thread, {"test_cases_messages": HumanMessage(content=feedback)})

        state = None
        for event in sdlc_workflow.stream(None, thread, stream_mode="values"):
            state = event
        
        logging.debug(f"Updated state: {state}")
        status = "completed" if state.get("test_cases_status") == 'approved' else state.get("test_cases_status", "pending")
        test_cases_messages = [serialize_message(msg) for msg in state.get("test_cases_messages", [])]
        
        # Initialize variables to avoid NameError
        qa_testing = None
        qa_testing_status = None
        qa_testing_messages = None
        deployment_steps = None
        deployment_status = None
        deployment_messages = None
        
        if status == "completed":
            qa_testing = state.get("qa_testing")
            qa_testing_status = state.get("qa_testing_status")
            qa_testing_messages = [serialize_message(msg) for msg in state.get("qa_testing_messages", [])]
            
            deployment_steps = state.get("deployment_steps")
            deployment_status_raw = state.get("deployment_status")
            deployment_status = "completed" if deployment_status_raw == 'approved' else deployment_status_raw
            deployment_messages = [serialize_message(msg) for msg in state.get("deployment_messages", [])]
            
        # Ensure test_cases is a list, not a tuple
        test_cases = state.get("test_cases", [])
        if isinstance(test_cases, tuple):
            test_cases = list(test_cases)
            
        session_data = {
            **session_data,
            "test_cases": test_cases,
            "test_cases_messages": test_cases_messages,
            "test_cases_status": status,
            "qa_testing": qa_testing if status == "completed" else None,
            "qa_testing_messages": qa_testing_messages if status == "completed" else None,
            "qa_testing_status": qa_testing_status if status == "completed" else None,
            "deployment_steps": deployment_steps if status == "completed" else None,
            "deployment_status": deployment_status if status == "completed" else None,
            "deployment_messages": deployment_messages if status == "completed" else None,
        }
        
        redis.set(session_id, json.dumps(session_data))
        logging.info(f"Test cases reviewed successfully for session: {session_id}")

        # Ensure test_cases is a list for the response
        test_cases_response = state.get("test_cases", [])
        if isinstance(test_cases_response, tuple):
            test_cases_response = list(test_cases_response)
        
        return TestCasesResponse.model_construct(
            session_id=session_id,
            status=status,
            test_cases=test_cases_response,
            messages=test_cases_messages
        )

    except Exception as e:
        logging.error(f"Error reviewing test cases: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

# # QA testing endpoints
@app.get("/qa/testing/get/{session_id}", response_model=QATestingResponse)
async def get_qa_testing(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Getting QA testing report for session: {session_id}")
    session_data = session_validator(session_id, redis, "qa_testing")
    
    try:
        qa_testing = session_data["qa_testing"]
        status = session_data["qa_testing_status"]
        messages = session_data["qa_testing_messages"]
        logging.info(f"QA testing results retrieved successfully for session: {session_id}")
        return QATestingResponse.model_construct(
            session_id=session_id,
            status=status,
            qa_testing=qa_testing,
            messages=messages
        )
        
    except Exception as e:
        logging.error(f"Error getting QA testing results: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))
    
    
# Deployment endpoints
@app.get("/deployment/get/{session_id}", response_model=DeploymentResponse)
async def get_deployment(
    session_id: str,
    redis: Redis = Depends(get_redis)
):
    logging.info(f"Getting deployment steps for session: {session_id}")
    session_data = session_validator(session_id, redis, "deployment")
    
    try:
        deployment_steps = session_data["deployment_steps"]
        status = session_data["deployment_status"]
        messages = session_data["deployment_messages"]
        logging.info(f"Deployment steps retrieved successfully for session: {session_id}")
        return DeploymentResponse.model_construct(
            session_id=session_id,
            status=status,
            deployment_steps=deployment_steps,
            messages=messages
        )
        
    except Exception as e:
        logging.error(f"Error getting deployment steps: {str(e)}")
        raise SDLCException(status_code=500, detail=str(e))

def session_validator(session_id: str, redis: Redis, current_node: str):
    session = redis.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = json.loads(session)
    if current_node == "user_story_review":
        if session_data["user_story_status"] == "completed":
            raise HTTPException(status_code=400, detail="User stories are already completed")
        
        if session_data["user_story_status"] != "pending_approval":
            raise HTTPException(status_code=400, detail="User stories are not pending approval")
    
    if current_node == "functional_generate":
        if session_data["user_story_status"] != "completed":
            raise HTTPException(status_code=400, detail="User stories are not completed")
        
    if current_node == "functional_review":
        if session_data["functional_status"] == "completed":
            raise HTTPException(status_code=400, detail="Functional documents are already completed")
        
        if session_data["functional_status"] != "pending_approval":
            raise HTTPException(status_code=400, detail="Functional documents are not pending approval")
        
    if current_node == "technical_generate":
        if session_data["functional_status"] != "completed":
            raise HTTPException(status_code=400, detail="Functional documents are not completed")
        
    if current_node == "technical_review":
        if session_data["technical_status"] == "completed":
            raise HTTPException(status_code=400, detail="Technical documents are already completed")
        
        if session_data["technical_status"] != "pending_approval":
            raise HTTPException(status_code=400, detail="Technical documents are not pending approval")
        
    if current_node == "frontend_generate":
        if session_data["technical_status"] != "completed":
            raise HTTPException(status_code=400, detail="Technical documents are not completed")
        
    if current_node == "frontend_review":
        if session_data["frontend_status"] == "completed":
            raise HTTPException(status_code=400, detail="Frontend code is already completed")
        
        if session_data["frontend_status"] != "pending_approval":
            raise HTTPException(status_code=400, detail="Frontend code is not pending approval")
        
    if current_node == "backend_generate":
        if session_data["frontend_status"] != "completed":
            raise HTTPException(status_code=400, detail="Frontend code is not completed")   
        
    if current_node == "backend_review":
        if session_data["backend_status"] == "completed":
            raise HTTPException(status_code=400, detail="Backend code is already completed")
        
        if session_data["backend_status"] != "pending_approval":
            raise HTTPException(status_code=400, detail="Backend code is not pending approval")
        
    if current_node == "security_review":
        if session_data["backend_status"] != "completed":
            raise HTTPException(status_code=400, detail="Backend code is not completed")
        
    if current_node == "test_cases_generate":
        if session_data["backend_status"] != "completed":
            raise HTTPException(status_code=400, detail="Backend code is not completed")
        
    if current_node == "test_cases_review":
        if session_data["test_cases_status"] == "completed":
            raise HTTPException(status_code=400, detail="Test cases are already completed")
        
    if current_node == "qa_testing":
        if session_data["test_cases_status"] != "completed":
            raise HTTPException(status_code=400, detail="Test cases are not completed")
        
    if current_node == "qa_testing_review":
        if session_data["qa_testing_status"] == "completed":
            raise HTTPException(status_code=400, detail="QA testing is already completed")
        
    return session_data
