# models/situation.py
from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EmergencyCategory(str, Enum):
    MEDICAL = "medical"
    FIRE = "fire"
    CRIME = "crime"
    TRAFFIC = "traffic_accident"
    DISASTER = "natural_disaster"
    INFRASTRUCTURE = "infrastructure"
    DOMESTIC = "domestic_disturbance"
    OTHER = "other"
    UNDETERMINED = "undetermined"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    LIFE_THREATENING = "life_threatening"

class SituationAnalysisOutput(BaseModel):
    emergency_category: EmergencyCategory = Field(description="The category of emergency situation")
    severity_level: SeverityLevel = Field(description="The assessed severity level of the situation")
    key_details: List[str] = Field(description="Key details extracted from the message")
    required_actions: List[str] = Field(description="Recommended actions to address the situation")
    required_resources: List[str] = Field(description="Resources that might be needed")
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    reasoning: str = Field(description="Explanation for the analysis provided")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())