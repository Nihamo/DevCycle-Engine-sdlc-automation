from pydantic import BaseModel, Field
from typing_extensions import Literal, List

class TestCase(BaseModel):
    test_id : str = Field(description="The id of the test case")
    description : str = Field(description="The description of the test case")
    steps : List[str] = Field(description="The steps of the test case")
    status : Literal["draft", "pass", "fail"] = Field(description="The status of the test case")