# agents/emotion_analyzer.py
import os
from typing import Optional
import langchain_google_genai as genai
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from models import EmotionAnalysisOutput, EmotionType, EmotionIntensity
from models import ContextEntry
from tools import ContextManagementTool
from config import GOOGLE_API_KEY, MODEL_NAME

# Set up Google Genai model
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = genai.ChatGoogleGenerativeAI(model=MODEL_NAME)

class EmotionAnalyzerAgent:
    def __init__(self, context_tool: ContextManagementTool):
        self.context_tool = context_tool
        self.tool_name = "EmotionAnalysisTool"
    
    def analyze(self, message: str) -> EmotionAnalysisOutput:
        """
        Analyze the emotional content of a message and store the result in context
        
        Args:
            message: The message to analyze
            
        Returns:
            The emotion analysis output
        """
        system_prompt = """You are an expert emotion analysis agent for an emergency response system. 
        Your task is to analyze the text from a caller and identify their emotional state.
        Focus on detecting emotions like fear, anger, sadness, distress, panic, confusion, and urgency.
        Assess the intensity of these emotions.
        
        Return your analysis in the exact format requested, as it will be used by other agents in the system.
        Be particularly attentive to signs of extreme distress or panic that might require priority handling.
        """
        
        human_prompt = f"""
        Analyze the emotional content of this message from someone contacting emergency services:
        
        MESSAGE: "{message}"
        
        Provide your analysis in a structured format.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        #output parser
        parser = PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)
        format_instructions = parser.get_format_instructions()
        
        #adding format instructions to the messages
        messages.append(HumanMessage(content=f"Format your response according to these instructions: {format_instructions}"))
        
        #model response will be returned as json 
        response = model.invoke(messages)
        # print(response)
        
        try:
            #parse converts the returned data structure to a pydantic structure 
            emotion_analysis = parser.parse(response.content)
            
            # Add to context management
            self.context_tool.add_entry(
                ContextEntry(
                    tool_name=self.tool_name,
                    data={
                        "primary_emotion": emotion_analysis.primary_emotion,
                        "secondary_emotion": emotion_analysis.secondary_emotion,
                        "intensity": emotion_analysis.intensity,
                        "confidence_score": emotion_analysis.confidence_score,
                        "reasoning": emotion_analysis.reasoning
                    }
                )
            )
            
            return emotion_analysis
            
        except Exception as e:
            print(f"Error parsing emotion analysis: {e}")
            print(f"Raw response: {response.content}")
            
            default_analysis = EmotionAnalysisOutput(
                primary_emotion=EmotionType.NEUTRAL,
                intensity=EmotionIntensity.MEDIUM,
                confidence_score=0.5,
                reasoning=f"Failed to parse model response: {str(e)}"
            )
            
            self.context_tool.add_entry(
                ContextEntry(
                    tool_name=self.tool_name,
                    data={
                        "primary_emotion": default_analysis.primary_emotion,
                        "intensity": default_analysis.intensity,
                        "confidence_score": default_analysis.confidence_score,
                        "error": str(e)
                    }
                )
            )
            
            return default_analysis