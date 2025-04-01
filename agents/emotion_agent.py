# agents/emotion_analyzer.py
import os
from typing import Optional, Dict, Any
from datetime import datetime
import langchain_google_genai as genai
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import ToolMessage
from models import (EmotionType, EmotionIntensity, EmotionAnalysisOutput, AudioEmotionOutput, AudioFeatures
                    , TemporalEmotionOutput, CrossModalValidationOutput, ContextEntry)
from tools import ContextManagementTool
from config import GOOGLE_API_KEY, MODEL_NAME
from tools import emotion_analysis_tools, AudioFeatureExtractorTool, AudioEmotionClassifierTool
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Google GenAI model
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = genai.ChatGoogleGenerativeAI(model=MODEL_NAME)

class EmotionAnalyzerAgent:
    def __init__(self, context_tool: ContextManagementTool):
        self.context_tool = context_tool
        self.tool_name = "EmotionAnalysisTool"
        # Bind tools to the model for tool-calling
        self.model_with_tools = model.bind_tools(emotion_analysis_tools)
        # Initialize audio tools for manual invocation
        self.audio_feature_extractor = AudioFeatureExtractorTool()
        self.audio_emotion_classifier = AudioEmotionClassifierTool()

    def analyze(self, message: str, audio_path: Optional[str] = None, timestamp: Optional[float] = None) -> EmotionAnalysisOutput:
        """
        Analyze the emotional content of a message and optionally audio, using tool-calling to decide which tools to use.

        Args:
            message: The message to analyze
            audio_path: Optional path to the audio file for analysis
            timestamp: Optional timestamp for temporal analysis (seconds since call start)

        Returns:
            The combined emotion analysis output
        """
        # System prompt for reasoning and tool selection
        system_prompt = """You are an expert emotion analysis agent for an emergency response system. 
        Your task is to analyze the emotional state of a caller based on their message and, if available, audio.
        Focus on detecting emotions like fear, anger, sadness, distress, panic, confusion, and urgency.
        Assess the intensity of these emotions.

        You have access to several tools to assist you:
        - AudioFeatureExtractor: Extracts audio features like pitch and volume. [Will be called automatically if audio is available]
        - AudioEmotionClassifier: Classifies emotions from audio features. [Will be called automatically if audio is available]
        - EmotionLexiconScorer: Scores emotions in text using a lexicon. Use for quick validation or low-confidence cases.
        - TemporalEmotionAnalyzerAdd: Adds an emotion analysis to the temporal history. Use when a timestamp is provided.
        - TemporalEmotionAnalyzerTrend: Analyzes emotional trends over time. Use after adding multiple emotion analyses.
        - CrossModalValidator: Validates consistency between text and audio analyses. Use when both text and audio analyses are available.

        First, perform a text-based emotion analysis. Then, decide which tools to use based on the input:
        - If timestamp is provided, use TemporalEmotionAnalyzerAdd and possibly TemporalEmotionAnalyzerTrend.
        - If both text and audio analyses are available, use CrossModalValidator.
        - Use EmotionLexiconScorer for validation if the text analysis confidence is low.

        Audio analysis will be handled automatically if an audio file is provided. Combine the results from text and audio analyses in your final output.

        Return your final analysis in the exact format requested, as it will be used by other agents in the system.
        Be particularly attentive to signs of extreme distress or panic that might require priority handling.
        """
        
        # Initial human prompt for text analysis
        human_prompt = f"""
        Analyze the emotional content of this message from someone contacting emergency services:
        
        MESSAGE: "{message}"
        
        Additional context:
        - Audio available: {"Yes" if audio_path else "No"}
        - Timestamp provided: {"Yes" if timestamp is not None else "No"}
        
        First, perform a text-based emotion analysis. Then, decide which tools to use based on the input and context.
        Provide your analysis in a structured format.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Output parser for the final result
        parser = PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)
        format_instructions = parser.get_format_instructions()
        messages.append(HumanMessage(content=f"Format your final response according to these instructions: {format_instructions}"))

        # Step 1: Perform audio analysis if audio_path is provided
        audio_analysis = None
        if audio_path:
            logger.info("Audio file provided, performing audio analysis...")
            try:
                # Extract audio features
                audio_features = self.audio_feature_extractor.extract(audio_path)
                logger.info(f"Audio features extracted: {audio_features}")
                
                # Classify emotions from audio features
                audio_analysis = self.audio_emotion_classifier.classify(audio_features)
                audio_analysis = AudioEmotionOutput(**audio_analysis)
                logger.info(f"Audio emotion analysis: {audio_analysis}")
                
                # Add audio analysis to the messages for the model to consider
                messages.append(HumanMessage(content=f"Audio analysis result: {audio_analysis.dict()}"))
            except Exception as e:
                logger.error(f"Error during audio analysis: {e}")
                audio_analysis = AudioEmotionOutput(
                    primary_emotion=EmotionType.NEUTRAL,
                    secondary_emotion=None,
                    intensity=EmotionIntensity.MEDIUM,
                    confidence_score=0.5,
                    reasoning=f"Error in audio analysis: {str(e)}",
                    analysis_timestamp=datetime.now().isoformat()
                )
                messages.append(HumanMessage(content=f"Audio analysis failed: {audio_analysis.dict()}"))

        # Step 2: Perform text-based analysis and decide on other tools
        tool_calls = []
        text_analysis = None
        lexicon_scores = None
        temporal_trend = None
        cross_modal_result = None

        while True:
            response = self.model_with_tools.invoke(messages)
            
            # Check if the model produced a final answer or tool calls
            if isinstance(response.content, str):
                try:
                    text_analysis = parser.parse(response.content)
                    break
                except Exception as e:
                    logger.error(f"Error parsing text emotion analysis: {e}")
                    text_analysis = EmotionAnalysisOutput(
                        primary_emotion=EmotionType.NEUTRAL,
                        secondary_emotion=None,
                        intensity=EmotionIntensity.MEDIUM,
                        confidence_score=0.5,
                        reasoning=f"Failed to parse model response: {str(e)}",
                        urgency=False,
                        analysis_timestamp=datetime.now().isoformat(),
                        call_timestamp=timestamp
                    )
                    break
            else:
                # Handle tool calls
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    logger.info(f"Tool called: {tool_name} with args: {tool_args}")

                    # Execute the tool
                    selected_tool = next((tool for tool in emotion_analysis_tools if tool.name == tool_name), None)
                    if not selected_tool:
                        logger.error(f"Tool {tool_name} not found.")
                        continue

                    try:
                        tool_result = selected_tool.func(**tool_args)
                        logger.info(f"Tool result: {tool_result}")

                        # Store results for later use
                        if tool_name == "EmotionLexiconScorer":
                            lexicon_scores = tool_result
                        elif tool_name == "TemporalEmotionAnalyzerAdd":
                            # Tool result is a status message
                            messages.append(HumanMessage(content=f"Temporal emotion added: {tool_result}. Consider analyzing the trend if enough data is available."))
                        elif tool_name == "TemporalEmotionAnalyzerTrend":
                            temporal_trend = TemporalEmotionOutput(**tool_result)
                        elif tool_name == "CrossModalValidator":
                            cross_modal_result = CrossModalValidationOutput(**tool_result)

                        # Add the tool result to the conversation
                        messages.append(ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        ))
                    except Exception as e:
                        logger.error(f"Error executing tool {tool_name}: {e}")
                        messages.append(ToolMessage(
                            content=f"Error: {str(e)}",
                            tool_call_id=tool_call["id"],
                            name=tool_name
                        ))

        # Step 3: Combine results and store in context
        if text_analysis is None:
            text_analysis = EmotionAnalysisOutput(
                primary_emotion=EmotionType.NEUTRAL,
                secondary_emotion=None,
                intensity=EmotionIntensity.MEDIUM,
                confidence_score=0.5,
                reasoning="Failed to generate text analysis.",
                urgency=False,
                analysis_timestamp=datetime.now().isoformat(),
                call_timestamp=timestamp
            )

        # Enhance reasoning with tool results
        if lexicon_scores:
            text_analysis.reasoning += f" | Lexicon scores: {lexicon_scores}"
        if audio_analysis:
            text_analysis.reasoning += f" | Audio analysis: {audio_analysis.dict()}"
        if cross_modal_result:
            text_analysis.reasoning += f" | Cross-modal validation: {cross_modal_result.dict()}"
        if temporal_trend:
            text_analysis.reasoning += f" | Temporal trend: {temporal_trend.trend}"

        # Store in context
        self.context_tool.add_entry(
            ContextEntry(
                tool_name=self.tool_name,
                data={
                    "primary_emotion": text_analysis.primary_emotion,
                    "secondary_emotion": text_analysis.secondary_emotion,
                    "intensity": text_analysis.intensity,
                    "confidence_score": text_analysis.confidence_score,
                    "reasoning": text_analysis.reasoning,
                    "lexicon_scores": lexicon_scores,
                    "audio_analysis": audio_analysis.dict() if audio_analysis else None,
                    "temporal_trend": temporal_trend.dict() if temporal_trend else None,
                    "cross_modal_result": cross_modal_result.dict() if cross_modal_result else None
                }
            )
        )

        return text_analysis