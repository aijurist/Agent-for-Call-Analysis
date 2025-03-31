# models/emotions.py
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EmotionType(str, Enum):
    FEAR = "fear"
    ANGER = "anger"
    SADNESS = "sadness"
    DISTRESS = "distress"
    PANIC = "panic"
    CALM = "calm"
    CONFUSED = "confused"
    URGENT = "urgent"
    NEUTRAL = "neutral"

class EmotionIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class EmotionAnalysisOutput(BaseModel):
    primary_emotion: EmotionType = Field(description="The primary emotion detected in the caller's message")
    secondary_emotion: Optional[EmotionType] = Field(None, description="A secondary emotion if present")
    intensity: EmotionIntensity = Field(description="The intensity level of the primary emotion")
    confidence_score: float = Field(description="Confidence score between 0 and 1")
    reasoning: str = Field(description="Explanation for why these emotions were detected")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())