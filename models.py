from sqlmodel import SQLModel, Field
from typing import Optional

class MindDump(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str  # The raw text the user dumps
    tasks: str    # We will store the AI-processed tasks here
    notes: str    # We will store the AI-processed notes here