import time
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from models import EmotionAnalysisOutput, SituationAnalysisOutput, ContextEntry
from tools import ContextManagementTool
from agents import EmotionAnalyzerAgent, SituationAnalyzerAgent
from config import CONTEXT_DATA_DIR

# Define the state for our graph using Pydantic
class GraphState(BaseModel):
    messages: List[HumanMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    emotion_result: Dict[str, Any] = Field(default_factory=dict)
    situation_result: Dict[str, Any] = Field(default_factory=dict)

# Global variables
emotion_analyzer: Optional[EmotionAnalyzerAgent] = None
situation_analyzer: Optional[SituationAnalyzerAgent] = None
context_tool: Optional[ContextManagementTool] = None

def initialize_agents() -> Tuple[EmotionAnalyzerAgent, SituationAnalyzerAgent, ContextManagementTool]:
    """Initialize the context tool and agents."""
    session_id = f"emergency_session_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    context_tool = ContextManagementTool(session_id, CONTEXT_DATA_DIR)
    emotion_analyzer = EmotionAnalyzerAgent(context_tool)
    situation_analyzer = SituationAnalyzerAgent(context_tool)
    return emotion_analyzer, situation_analyzer, context_tool

def run_emotion_analysis(state: GraphState) -> Dict[str, Any]:
    """Run emotion analysis on the latest message."""
    global emotion_analyzer
    print("\n[1/2] Running emotion analysis...")
    start_time = time.time()
    
    latest_message = state.messages[-1].content
    emotion_result = emotion_analyzer.analyze(latest_message)
    
    result = {
        "emotion_result": {
            "primary_emotion": emotion_result.primary_emotion,
            "secondary_emotion": emotion_result.secondary_emotion,
            "intensity": emotion_result.intensity,
            "confidence_score": emotion_result.confidence_score,
            "reasoning": emotion_result.reasoning,
        }
    }
    
    print(f"Emotion analysis completed in {time.time() - start_time:.2f} seconds")
    return result

def run_situation_analysis(state: GraphState) -> Dict[str, Any]:
    """Run situation analysis on the latest message."""
    global situation_analyzer
    print("\n[2/2] Running situation assessment...")
    start_time = time.time()
    
    latest_message = state.messages[-1].content
    situation_result = situation_analyzer.analyze(latest_message)
    
    result = {
        "situation_result": {
            "emergency_category": situation_result.emergency_category,
            "severity_level": situation_result.severity_level,
            "key_details": situation_result.key_details,
            "required_actions": situation_result.required_actions,
            "required_resources": situation_result.required_resources,
            "confidence_score": situation_result.confidence_score,
            "reasoning": situation_result.reasoning,
        }
    }
    
    print(f"Situation assessment completed in {time.time() - start_time:.2f} seconds")
    return result

def combine_results(state: GraphState) -> Dict[str, Any]:
    """Combine results from both analyses and update the context."""
    global context_tool
    context_entries = context_tool.get_entries()
    
    result = {
        "context": {
            "emotion_analysis": state.emotion_result,
            "situation_analysis": state.situation_result,
            "context_entries": [entry.dict() for entry in context_entries],
        }
    }
    return result

def display_results(result: Dict[str, Any]) -> None:
    """Display the results of both analyses."""
    print("\n=== ANALYSIS RESULTS ===")
    
    print("\nEmotion Analysis:")
    if "emotion_result" in result and result["emotion_result"]:
        emotion_result = result["emotion_result"]
        print(f"Primary emotion: {emotion_result['primary_emotion']}")
        if emotion_result.get('secondary_emotion'):
            print(f"Secondary emotion: {emotion_result['secondary_emotion']}")
        print(f"Intensity: {emotion_result['intensity']}")
        print(f"Confidence: {emotion_result['confidence_score']:.2f}")
        print(f"Reasoning: {emotion_result['reasoning']}")
    else:
        print("No emotion analysis results available")
    
    print("\nSituation Assessment:")
    if "situation_result" in result and result["situation_result"]:
        situation_result = result["situation_result"]
        print(f"Emergency Category: {situation_result['emergency_category']}")
        print(f"Severity Level: {situation_result['severity_level']}")
        print("\nKey Details:")
        for detail in situation_result['key_details']:
            print(f"- {detail}")
        print("\nRequired Actions:")
        for action in situation_result['required_actions']:
            print(f"- {action}")
        print("\nRequired Resources:")
        for resource in situation_result['required_resources']:
            print(f"- {resource}")
        print(f"\nConfidence: {situation_result['confidence_score']:.2f}")
        print(f"Reasoning: {situation_result['reasoning']}")
    else:
        print("No situation analysis results available")
    
    print("\n=== CURRENT CONTEXT ===")
    context_entries = result.get("context", {}).get("context_entries", [])
    if context_entries:
        for idx, entry in enumerate(context_entries):
            print(f"\nEntry {idx+1} - {entry.get('tool_name', 'Unknown')} ({entry.get('timestamp', 'N/A')}:")
            for key, value in entry.get('data', {}).items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    - {item}")
                else:
                    print(f"  {key}: {value}")
    else:
        print("No context entries available")

def create_graph() -> StateGraph:
    """Create the LangGraph workflow."""
    graph = StateGraph(GraphState)
    
    graph.add_node("run_emotion_analysis", run_emotion_analysis)
    graph.add_node("run_situation_analysis", run_situation_analysis)
    graph.add_node("combine_results", combine_results)
    
    graph.add_edge("run_emotion_analysis", "run_situation_analysis")
    graph.add_edge("run_situation_analysis", "combine_results")
    graph.add_edge("combine_results", END)
    
    graph.set_entry_point("run_emotion_analysis")
    
    return graph

# Initialize agents and compile the graph at the module level
emotion_analyzer, situation_analyzer, context_tool = initialize_agents()
compiled_app = create_graph().compile()

def main():
    """Run the CLI with the compiled graph."""
    print("Emergency Response System")
    print("Enter emergency messages (type 'exit' to quit):")
    
    try:
        while True:
            user_input = input("\nEmergency message: ")
            if user_input.lower() == 'exit':
                break
            
            print("\n=== ANALYZING EMERGENCY MESSAGE ===")
            state = GraphState(messages=[HumanMessage(content=user_input)])
            result = compiled_app.invoke(state)
            display_results(result)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Emergency Response System")
    parser.add_argument("--server-only", action="store_true", help="Run only the server without the CLI")
    
    args = parser.parse_args()
    
    if args.server_only:
        # For server-only mode, just let langgraph dev handle it
        print("Running in server-only mode. Use 'langgraph dev' to start the server.")
    else:
        main()