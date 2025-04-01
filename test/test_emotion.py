# test_emotion_analyzer.py
import os
from agents import EmotionAnalyzerAgent
from tools import ContextManagementTool
import logging
from datetime import datetime

# Set up logging to see the agent's reasoning and tool usage
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_emotion_analyzer():
    # Initialize the context tool and agent
    context_tool = ContextManagementTool("001")
    emotion_analyzer = EmotionAnalyzerAgent(context_tool)

    # Define the test inputs
    audio_path = "test.mp3"  # Path to your audio file
    message = "I'm really scared, please help me!"  # Optional: Simulated text message
    timestamp = 10.0  # Optional: Simulated timestamp (seconds since call start)

    # Ensure the audio file exists
    if not os.path.exists(audio_path):
        logger.error(f"Audio file {audio_path} not found.")
        return

    # Run the analysis
    logger.info("Starting emotion analysis...")
    try:
        result = emotion_analyzer.analyze(
            message=message,
            audio_path=audio_path,
            timestamp=timestamp
        )
        logger.info("Emotion analysis completed successfully.")
        
        # Print the results
        print("\n=== Emotion Analysis Result ===")
        print(f"Primary Emotion: {result.primary_emotion}")
        print(f"Secondary Emotion: {result.secondary_emotion}")
        print(f"Intensity: {result.intensity}")
        print(f"Confidence Score: {result.confidence_score}")
        print(f"Urgency: {result.urgency}")
        print(f"Reasoning: {result.reasoning}")
        print(f"Analysis Timestamp: {result.analysis_timestamp}")
        print(f"Call Timestamp: {result.call_timestamp}")
        
        # Optionally, print the context to see what was stored
        print("\n=== Context Data ===")
        context_data = context_tool.get_entries()
        for entry in context_data:
            print(entry)
            
    except Exception as e:
        logger.error(f"Error during emotion analysis: {e}")

if __name__ == "__main__":
    test_emotion_analyzer()