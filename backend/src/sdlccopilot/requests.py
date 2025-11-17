from pydantic import BaseModel, Field
from typing_extensions import List


class ProjectRequirementsRequest(BaseModel):
    title : str = Field(description="Title of the project")
    description : str = Field(description="Description of the project")
    requirements : List[str] = Field(description="Requirements of the project")

class OwnerFeedbackRequest(BaseModel):
    feedback: str = Field(default='approved', description="Feedback from the owner")