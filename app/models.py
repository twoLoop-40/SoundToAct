"""
Pydantic Models for API
"""
from pydantic import BaseModel, Field
from typing import Optional


class KeywordActionCreate(BaseModel):
    """Model for creating a new keyword-action mapping"""

    keyword: str = Field(..., min_length=1, description="The keyword to detect")
    action_type: str = Field(
        ..., description="Type of action (call, music, lights, custom)"
    )
    action_params: Optional[dict] = Field(
        default=None, description="Additional parameters for the action"
    )


class KeywordActionResponse(BaseModel):
    """Model for keyword-action response"""

    keyword: str
    action_type: str
    action_params: Optional[dict] = None
    is_active: bool = True


class ListenRequest(BaseModel):
    """Model for listen request"""

    timeout: int = Field(default=5, ge=1, le=30, description="Timeout in seconds")
    phrase_time_limit: int = Field(
        default=5, ge=1, le=30, description="Phrase time limit in seconds"
    )


class ListenResponse(BaseModel):
    """Model for listen response"""

    recognized_text: str
    triggered_keywords: list[str]
    success: bool
    action_messages: list[str] = Field(default_factory=list, description="Messages from triggered actions")


class StatusResponse(BaseModel):
    """Model for status response"""

    is_listening: bool
    registered_keywords: list[str]
    message: str