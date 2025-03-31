# models/context.py
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ContextEntry(BaseModel):
    tool_name: str = Field(description="Name of the tool that added this context")
    data: Dict[str, Any] = Field(description="The actual context data")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())