# models/emotions.py
from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class EmotionType(str, Enum):
    FEAR = "fear"
    ANGER = "anger"
    SADNESS = "sadness"
    DISTRESS = "distress"
    PANIC = "panic"
    CONFUSED = "confused"
    NEUTRAL = "neutral"
    # Removed URGENT (moved to a separate field) and CALM (replaced with NEUTRAL)

class EmotionIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class TrendType(str, Enum):
    ESCALATING = "escalating"
    DEESCALATING = "deescalating"
    STABLE = "stable"
    UNKNOWN = "unknown"

class RecommendedAction(str, Enum):
    PROCEED = "proceed"
    REANALYZE = "reanalyze"
    ESCALATE = "escalate"
    FLAG = "flag"

class EmotionAnalysisOutput(BaseModel):
    primary_emotion: EmotionType = Field(description="The primary emotion detected in the caller's message")
    secondary_emotion: Optional[EmotionType] = Field(None, description="A secondary emotion if present")
    intensity: EmotionIntensity = Field(description="The intensity level of the primary emotion")
    confidence_score: float = Field(description="Confidence score between 0 and 1", ge=0.0, le=1.0)
    reasoning: str = Field(description="Explanation for why these emotions were detected")
    urgency: bool = Field(default=False, description="Whether the message indicates urgency (e.g., time-sensitive emergency)")
    analysis_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp of when the analysis was performed")
    call_timestamp: Optional[float] = Field(None, description="Relative timestamp within the call in seconds")

class AudioFeatures(BaseModel):
    pitch: float = Field(..., description="Average pitch of the audio in Hz", ge=0.0, le=1000.0)  # Typical human range
    volume: float = Field(..., description="Average volume (RMS energy) of the audio", ge=0.0)
    speech_rate: float = Field(..., description="Speech rate in syllables per second (approximated via zero-crossings)", ge=0.0)
    prosody_variance: float = Field(..., description="Variance in pitch for prosody analysis", ge=0.0)

class AudioEmotionOutput(BaseModel):
    primary_emotion: EmotionType = Field(..., description="Primary emotion detected from audio")
    secondary_emotion: Optional[EmotionType] = Field(None, description="A secondary emotion if present")
    intensity: EmotionIntensity = Field(..., description="Intensity of the primary emotion")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the emotion prediction")
    reasoning: str = Field(..., description="Explanation of the emotion analysis")
    analysis_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp of when the analysis was performed")

class TemporalEmotionEntry(BaseModel):
    timestamp: float = Field(..., description="Relative timestamp within the call in seconds", ge=0.0)
    primary_emotion: EmotionType = Field(..., description="Primary emotion at this timestamp")
    intensity: EmotionIntensity = Field(..., description="Intensity of the emotion")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the prediction")

class TemporalEmotionOutput(BaseModel):
    history: List[TemporalEmotionEntry] = Field(..., description="List of emotion entries over time")
    trend: TrendType = Field(..., description="The emotional trend (e.g., escalating distress)")

class CrossModalValidationOutput(BaseModel):
    is_consistent: bool = Field(..., description="Whether text and audio analyses are consistent")
    discrepancy_reason: Optional[str] = Field(None, description="Reason for any discrepancy")
    recommended_action: RecommendedAction = Field(..., description="Recommended action (e.g., escalate, re-analyze)")
    analysis_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp of when the validation was performed")