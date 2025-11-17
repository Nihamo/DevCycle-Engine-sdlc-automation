from typing_extensions import TypedDict, Annotated, List, Literal
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langgraph.graph import add_messages
from typing import Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field

class ProjectRequirements(BaseModel):
    title: str = Field(description="The title of the project")
    description: str = Field(description="The description of the project")
    requirements : List[str] = Field(description="The requirements of the project")

## User story
class UserStory(BaseModel):
    story_id : str = Field(description="The id of the user story")
    title : str = Field(description="The title of the user story")
    description : str = Field(description="The description of the user story")
    acceptance_criteria : List[str] = Field(description="The acceptance criteria of the user story")
