# emotion_tools.py
import os
import numpy as np
import librosa
import logging
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain.tools import Tool
import langchain_google_genai as genai
from models import EmotionType, EmotionIntensity, EmotionAnalysisOutput, AudioFeatures, AudioEmotionOutput, TemporalEmotionEntry, TemporalEmotionOutput, CrossModalValidationOutput, TrendType, RecommendedAction
from config import GOOGLE_API_KEY, MODEL_NAME
from datetime import datetime

# Set up logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Google GenAI model
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = genai.ChatGoogleGenerativeAI(model=MODEL_NAME)

# Sample emotion lexicon for quick scoring
EMOTION_LEXICON = {
    "scared": {"emotion": EmotionType.FEAR, "weight": 0.9},
    "help": {"emotion": EmotionType.DISTRESS, "weight": 0.8},
    "angry": {"emotion": EmotionType.ANGER, "weight": 0.7},
    "hurt": {"emotion": EmotionType.SADNESS, "weight": 0.6},
    "confused": {"emotion": EmotionType.CONFUSED, "weight": 0.5},
    "panic": {"emotion": EmotionType.PANIC, "weight": 0.95},
}

class AudioFeatureExtractorTool:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def extract(self, audio_path: str) -> dict:
        try:
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            # Extract pitch using piptrack
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
            # Flatten pitches and filter out zeros
            non_zero_pitches = pitches[pitches > 0]
            pitch = np.nanmean(non_zero_pitches) if non_zero_pitches.size > 0 else 0.0
            
            # Extract volume (RMS energy)
            volume = np.mean(librosa.feature.rms(y=audio))
            
            # Estimate speech rate (simplified: number of zero-crossings as a proxy for syllables)
            zero_crossings = librosa.zero_crossings(audio, pad=False)
            speech_rate = len(zero_crossings) / (len(audio) / sr)
            
            # Prosody variance (variance in pitch)
            prosody_variance = np.var(non_zero_pitches) if non_zero_pitches.size > 0 else 0.0
            
            features = AudioFeatures(
                pitch=float(pitch),
                volume=float(volume),
                speech_rate=float(speech_rate),
                prosody_variance=float(prosody_variance)
            )
            logger.info(f"Extracted audio features: {features}")
            return features.dict()
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            return AudioFeatures(pitch=0.0, volume=0.0, speech_rate=0.0, prosody_variance=0.0).dict()

class AudioEmotionClassifierTool:
    def __init__(self):
        self.pitch_thresholds = {"high": 200, "low": 100}
        self.volume_thresholds = {"high": 0.1, "low": 0.05}
        self.speech_rate_thresholds = {"fast": 5.0, "slow": 2.0}

    def classify(self, features: dict) -> dict:
        try:
            features = AudioFeatures(**features)
            if features.pitch > self.pitch_thresholds["high"] and features.speech_rate > self.speech_rate_thresholds["fast"]:
                primary_emotion = EmotionType.PANIC
                intensity = EmotionIntensity.HIGH
                confidence = 0.9
                reasoning = "High pitch and fast speech rate indicate panic."
            elif features.volume > self.volume_thresholds["high"]:
                primary_emotion = EmotionType.DISTRESS
                intensity = EmotionIntensity.HIGH
                confidence = 0.85
                reasoning = "High volume suggests distress."
            elif features.pitch < self.pitch_thresholds["low"]:
                primary_emotion = EmotionType.SADNESS
                intensity = EmotionIntensity.MEDIUM
                confidence = 0.7
                reasoning = "Low pitch indicates sadness."
            else:
                primary_emotion = EmotionType.NEUTRAL
                intensity = EmotionIntensity.MEDIUM
                confidence = 0.5
                reasoning = "No strong emotional cues detected in audio."

            output = AudioEmotionOutput(
                primary_emotion=primary_emotion,
                secondary_emotion=None,
                intensity=intensity,
                confidence_score=confidence,
                reasoning=reasoning,
                analysis_timestamp=datetime.now().isoformat()
            )
            logger.info(f"Audio emotion classification: {output}")
            return output.dict()
        except Exception as e:
            logger.error(f"Error classifying audio emotion: {e}")
            return AudioEmotionOutput(
                primary_emotion=EmotionType.NEUTRAL,
                secondary_emotion=None,
                intensity=EmotionIntensity.MEDIUM,
                confidence_score=0.5,
                reasoning=f"Error in classification: {str(e)}",
                analysis_timestamp=datetime.now().isoformat()
            ).dict()

class EmotionLexiconScorerTool:
    def score(self, text: str) -> dict:
        try:
            emotion_scores = {emotion.value: 0.0 for emotion in EmotionType}
            words = text.lower().split()
            for word in words:
                if word in EMOTION_LEXICON:
                    emotion = EMOTION_LEXICON[word]["emotion"]
                    weight = EMOTION_LEXICON[word]["weight"]
                    emotion_scores[emotion.value] += weight
            logger.info(f"Lexicon-based emotion scores: {emotion_scores}")
            return emotion_scores
        except Exception as e:
            logger.error(f"Error in lexicon scoring: {e}")
            return {emotion.value: 0.0 for emotion in EmotionType}

class TemporalEmotionAnalyzerTool:
    def __init__(self):
        self.emotion_history: List[TemporalEmotionEntry] = []

    def add_emotion(self, emotion_output: dict, timestamp: float) -> dict:
        try:
            emotion_output = EmotionAnalysisOutput(**emotion_output)
            entry = TemporalEmotionEntry(
                timestamp=timestamp,
                primary_emotion=emotion_output.primary_emotion,
                intensity=emotion_output.intensity,
                confidence_score=emotion_output.confidence_score
            )
            self.emotion_history.append(entry)
            logger.info(f"Added temporal emotion entry: {entry}")
            return {"status": "success", "message": "Emotion entry added."}
        except Exception as e:
            logger.error(f"Error adding temporal emotion entry: {e}")
            return {"status": "error", "message": str(e)}

    def analyze_trend(self) -> dict:
        try:
            if len(self.emotion_history) < 2:
                return TemporalEmotionOutput(
                    history=self.emotion_history,
                    trend=TrendType.UNKNOWN
                ).dict()

            distress_emotions = [EmotionType.DISTRESS, EmotionType.PANIC, EmotionType.FEAR]
            intensities = [
                entry.intensity for entry in self.emotion_history
                if entry.primary_emotion in distress_emotions
            ]
            if intensities and intensities[-1] > intensities[0]:
                trend = TrendType.ESCALATING
            elif intensities and intensities[-1] < intensities[0]:
                trend = TrendType.DEESCALATING
            else:
                trend = TrendType.STABLE

            output = TemporalEmotionOutput(history=self.emotion_history, trend=trend)
            logger.info(f"Temporal emotion trend: {trend}")
            return output.dict()
        except Exception as e:
            logger.error(f"Error analyzing temporal trend: {e}")
            return TemporalEmotionOutput(
                history=self.emotion_history,
                trend=TrendType.UNKNOWN
            ).dict()

class CrossModalValidatorTool:
    def validate(self, text_analysis: dict, audio_analysis: dict) -> dict:
        try:
            text_analysis = EmotionAnalysisOutput(**text_analysis)
            audio_analysis = AudioEmotionOutput(**audio_analysis)
            is_consistent = text_analysis.primary_emotion == audio_analysis.primary_emotion
            if is_consistent:
                return CrossModalValidationOutput(
                    is_consistent=True,
                    discrepancy_reason=None,
                    recommended_action=RecommendedAction.PROCEED,
                    analysis_timestamp=datetime.now().isoformat()
                ).dict()

            distress_emotions = [EmotionType.DISTRESS, EmotionType.PANIC, EmotionType.FEAR]
            if audio_analysis.primary_emotion in distress_emotions and audio_analysis.confidence_score > text_analysis.confidence_score:
                discrepancy_reason = "Audio indicates distress not detected in text, possibly due to transcription error."
                recommended_action = RecommendedAction.ESCALATE
            elif text_analysis.confidence_score > audio_analysis.confidence_score:
                discrepancy_reason = "Text analysis more confident; audio may be noisy."
                recommended_action = RecommendedAction.FLAG
            else:
                discrepancy_reason = "Unclear discrepancy between text and audio analyses."
                recommended_action = RecommendedAction.REANALYZE

            output = CrossModalValidationOutput(
                is_consistent=False,
                discrepancy_reason=discrepancy_reason,
                recommended_action=recommended_action,
                analysis_timestamp=datetime.now().isoformat()
            )
            logger.info(f"Cross-modal validation result: {output}")
            return output.dict()
        except Exception as e:
            logger.error(f"Error in cross-modal validation: {e}")
            return CrossModalValidationOutput(
                is_consistent=False,
                discrepancy_reason=f"Error in validation: {str(e)}",
                recommended_action=RecommendedAction.ESCALATE,
                analysis_timestamp=datetime.now().isoformat()
            ).dict()

# Instantiate tool objects
audio_feature_extractor_tool = AudioFeatureExtractorTool()
audio_emotion_classifier_tool = AudioEmotionClassifierTool()
emotion_lexicon_scorer_tool = EmotionLexiconScorerTool()
temporal_emotion_analyzer_tool = TemporalEmotionAnalyzerTool()
cross_modal_validator_tool = CrossModalValidatorTool()

# Define LangChain Tools
emotion_analysis_tools = [
    Tool(
        name="AudioFeatureExtractor",
        func=audio_feature_extractor_tool.extract,
        description="Extracts audio features like pitch, volume, and speech rate from an audio file. Use this when audio is available to analyze emotional cues in the caller's voice."
    ),
    Tool(
        name="AudioEmotionClassifier",
        func=audio_emotion_classifier_tool.classify,
        description="Classifies emotions from audio features. Use this after extracting audio features to determine emotions like panic or distress from the caller's voice."
    ),
    Tool(
        name="EmotionLexiconScorer",
        func=emotion_lexicon_scorer_tool.score,
        description="Scores emotions in text using a predefined lexicon. Use this for quick validation of text-based emotion analysis or when model confidence is low."
    ),
    Tool(
        name="TemporalEmotionAnalyzerAdd",
        func=temporal_emotion_analyzer_tool.add_emotion,
        description="Adds an emotion analysis to the temporal history. Use this to track emotions over time during a call, especially if a timestamp is provided."
    ),
    Tool(
        name="TemporalEmotionAnalyzerTrend",
        func=temporal_emotion_analyzer_tool.analyze_trend,
        description="Analyzes the trend of emotions over time. Use this to detect patterns like escalating distress after multiple emotion analyses have been added."
    ),
    Tool(
        name="CrossModalValidator",
        func=cross_modal_validator_tool.validate,
        description="Validates consistency between text and audio emotion analyses. Use this when both text and audio analyses are available to ensure reliability."
    )
]