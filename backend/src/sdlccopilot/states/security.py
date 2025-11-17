from pydantic import BaseModel, Field
from typing_extensions import Literal


class SecurityReview(BaseModel):
    sec_id : str = Field(description="The id of the security review")
    review : str = Field(description="The review of the security review")
    file_path : str = Field(description="The file path of the security review")
    recommendation : str = Field(description="The recommendation of the security review")
    priority : Literal["high", "medium", "low"] = Field(description="The priority of the security review")