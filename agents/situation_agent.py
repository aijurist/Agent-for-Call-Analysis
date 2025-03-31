# agents/situation_analyzer.py
import os
from typing import Optional, List
import langchain_google_genai as genai
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from models import SituationAnalysisOutput, EmergencyCategory, SeverityLevel
from models import ContextEntry
from tools import ContextManagementTool
from config import GOOGLE_API_KEY, MODEL_NAME

# Set up Google Genai model
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = genai.ChatGoogleGenerativeAI(model=MODEL_NAME)

class SituationAnalyzerAgent:
    def __init__(self, context_tool: ContextManagementTool):
        self.context_tool = context_tool
        self.tool_name = "SituationAnalysisTool"
    
    def analyze(self, message: str) -> SituationAnalysisOutput:
        """
        Analyze the situation described in an emergency message
        
        Args:
            message: The emergency message to analyze
            
        Returns:
            The situation analysis output
        """
        # Get emotion analysis from context if available
        emotion_entry = self.context_tool.get_latest_entry("EmotionAnalysisTool")
        emotion_context = ""
        if emotion_entry:
            emotion_context = f"""
            Previous emotion analysis detected:
            - Primary emotion: {emotion_entry.data.get('primary_emotion', 'N/A')}
            - Secondary emotion: {emotion_entry.data.get('secondary_emotion', 'N/A')}
            - Intensity: {emotion_entry.data.get('intensity', 'N/A')}
            - Confidence: {emotion_entry.data.get('confidence_score', 'N/A')}
            """
        
        system_prompt = """You are an expert situation assessment agent for an emergency response system.
        Your task is to analyze emergency messages and determine:
        1. The type of emergency situation
        2. The severity level
        3. Key details about the situation
        4. Necessary response actions
        5. Any resources that might be required
        
        Focus on identifying critical information while maintaining a high degree of accuracy.
        Return your analysis in the exact format requested, as it will be used by other agents in the system.
        """
        
        human_prompt = f"""
        Analyze this emergency message:
        
        MESSAGE: "{message}"
        
        {emotion_context}
        
        Categorize the emergency, assess severity, identify key details, and recommend appropriate actions.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Create output parser
        parser = PydanticOutputParser(pydantic_object=SituationAnalysisOutput)
        format_instructions = parser.get_format_instructions()
        
        # Add format instructions to the prompt
        messages.append(HumanMessage(content=f"Format your response according to these instructions: {format_instructions}"))
        
        # Get response from the model
        response = model.invoke(messages)
        
        # Parse the response
        try:
            situation_analysis = parser.parse(response.content)
            
            # Add to context management
            self.context_tool.add_entry(
                ContextEntry(
                    tool_name=self.tool_name,
                    data={
                        "emergency_category": situation_analysis.emergency_category,
                        "severity_level": situation_analysis.severity_level,
                        "key_details": situation_analysis.key_details,
                        "required_actions": situation_analysis.required_actions,
                        "required_resources": situation_analysis.required_resources,
                        "confidence_score": situation_analysis.confidence_score,
                        "reasoning": situation_analysis.reasoning
                    }
                )
            )
            
            return situation_analysis
            
        except Exception as e:
            print(f"Error parsing situation analysis: {e}")
            print(f"Raw response: {response.content}")
            
            default_analysis = SituationAnalysisOutput(
                emergency_category=EmergencyCategory.UNDETERMINED,
                severity_level=SeverityLevel.MEDIUM,
                key_details=["Unable to parse emergency details"],
                required_actions=["Escalate to human operator for review"],
                required_resources=["Human intervention required"],
                confidence_score=0.3,
                reasoning=f"Failed to parse model response: {str(e)}"
            )
            
            self.context_tool.add_entry(
                ContextEntry(
                    tool_name=self.tool_name,
                    data={
                        "emergency_category": default_analysis.emergency_category,
                        "severity_level": default_analysis.severity_level,
                        "key_details": default_analysis.key_details,
                        "error": str(e)
                    }
                )
            )
            
            return default_analysis