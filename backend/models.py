"""
==========================================================
AccountaAI - Pydantic Models
----------------------------------------------------------
Defines all structured models used throughout the project.
==========================================================
"""

from typing import List
from pydantic import BaseModel, Field


# ==========================================================
# Individual Task Model
# ==========================================================

class Task(BaseModel):
    task: str = Field(
        description="Short description of the task."
    )

    owner: str = Field(
        default="Unassigned",
        description="Person responsible for completing the task."
    )

    deadline: str = Field(
        default="Not Specified",
        description="Deadline for the task."
    )

    priority: str = Field(
        default="Medium",
        description="Critical | High | Medium | Low"
    )

    status: str = Field(
        default="Pending",
        description="Pending | In Progress | Completed"
    )


# ==========================================================
# Meeting Analysis Model
# ==========================================================

class MeetingAnalysis(BaseModel):
    summary: str = Field(
        default="",
        description="Concise meeting summary."
    )

    decisions: List[str] = Field(
        default_factory=list,
        description="Important decisions taken during the meeting."
    )

    tasks: List[Task] = Field(
        default_factory=list,
        description="Action items extracted from the meeting."
    )

    risks: List[str] = Field(
        default_factory=list,
        description="Potential risks discussed."
    )

    follow_ups: List[str] = Field(
        default_factory=list,
        description="Follow-up items after the meeting."
    )

    accountability_score: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Overall accountability score."
    )