from typing_extensions import List, Optional
from pydantic import BaseModel, Field

class TestResult(BaseModel):
    """Model for individual test result"""
    test_id: str = Field(..., description="Unique identifier for the test case")
    description: str = Field(..., description="Brief description of what the test case verifies")
    status: str = Field(..., description="Status of the test case (pass/fail)")
    actual_result: str = Field(..., description="Detailed explanation of what actually happened")
    expected_result: str = Field(..., description="What was expected to happen")
    failure_reason: Optional[str] = Field(None, description="Explanation of why the test failed, if applicable")

class TestSummary(BaseModel):
    """Model for test summary statistics"""
    total_tests: int = Field(..., description="Total number of tests executed")
    passed: int = Field(..., description="Number of tests that passed")
    failed: int = Field(..., description="Number of tests that failed")
    pass_percentage: float = Field(..., description="Percentage of tests that passed")

class QATesting(BaseModel):
    """Model for complete QA testing results"""
    summary: TestSummary = Field(..., description="Summary statistics of the test execution") 
    test_results: List[TestResult] = Field(..., description="List of individual test results")
