# 🚨 LangChain Voice Agent - Emergency Response System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Under Development](https://img.shields.io/badge/status-under%20development-orange.svg)](https://github.com/yourusername/langchain_voice_agent)

> ⚠️ **This project is currently under active development.** Features, APIs, and documentation may change without notice. Use in production environments is not recommended at this time.

## 📋 Overview

The LangChain Voice Agent is an AI-powered emergency response analysis system that combines text and audio analysis to assess emergency situations. Using LangChain, LangGraph, and Google's Gemini AI, this system can:

- **Analyze emotions** from text messages and audio input (fear, panic, distress, etc.)
- **Assess emergency situations** and categorize them (medical, fire, crime, etc.)
- **Track emotional trends** over time during emergency calls
- **Perform cross-modal validation** between text and audio analyses
- **Provide actionable insights** for emergency responders

## ✨ Features

### 🎭 Emotion Analysis
- Multi-modal emotion detection (text + audio)
- Real-time emotion intensity assessment
- Temporal emotion tracking and trend analysis
- Audio feature extraction (pitch, volume, speech rate, prosody)
- Emotion lexicon scoring for quick validation
- Cross-modal validation between text and audio

### 🚑 Situation Assessment
- Emergency categorization (medical, fire, crime, traffic, disaster, etc.)
- Severity level detection (low, medium, high, critical, life-threatening)
- Key detail extraction from emergency messages
- Recommended action generation
- Required resource identification

### 🔄 Workflow Orchestration
- LangGraph-based agent orchestration
- Context management across analysis steps
- Session-based data persistence
- Parallel analysis execution

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Emergency Message Input         │
│        (Text + Optional Audio)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         LangGraph Workflow              │
│  ┌───────────────────────────────────┐  │
│  │   1. Emotion Analysis Agent       │  │
│  │      - Text Analysis              │  │
│  │      - Audio Analysis (if avail)  │  │
│  │      - Temporal Tracking          │  │
│  │      - Cross-Modal Validation     │  │
│  └──────────────┬────────────────────┘  │
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │   2. Situation Analysis Agent     │  │
│  │      - Emergency Categorization   │  │
│  │      - Severity Assessment        │  │
│  │      - Action Recommendations     │  │
│  └──────────────┬────────────────────┘  │
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │   3. Context Aggregation          │  │
│  │      - Result Combination         │  │
│  │      - Session Management         │  │
│  └───────────────────────────────────┘  │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│     Structured Analysis Output          │
│  (JSON with emotions + situation data)  │
└─────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini AI)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aijurist/Agent-for-Call-Analysis.git
   cd Agent-for-Call-Analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   MODEL_NAME=gemini-1.5-flash
   ```

   To get a Google API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create and copy your API key

### Usage

#### CLI Mode (Interactive)

Run the emergency response system in interactive CLI mode:

```bash
python main.py
```

Enter emergency messages when prompted:
```
Emergency Response System
Enter emergency messages (type 'exit' to quit):

Emergency message: Help! There's a fire in the building on 5th floor!
```

The system will analyze both the emotion and situation, displaying:
- Primary and secondary emotions detected
- Emotion intensity and confidence
- Emergency category and severity
- Key details and recommended actions
- Required resources

#### LangGraph Server Mode

Run as a LangGraph development server for API access:

```bash
langgraph dev
```

This starts a server that you can interact with via the LangGraph API.

#### Programmatic Usage

```python
from agents import EmotionAnalyzerAgent, SituationAnalyzerAgent
from tools import ContextManagementTool
from langchain_core.messages import HumanMessage

# Initialize context and agents
context_tool = ContextManagementTool("session_123", "./context_data/")
emotion_agent = EmotionAnalyzerAgent(context_tool)
situation_agent = SituationAnalyzerAgent(context_tool)

# Analyze an emergency message
message = "Help! Someone broke into my house!"

# Emotion analysis
emotion_result = emotion_agent.analyze(message)
print(f"Emotion: {emotion_result.primary_emotion} ({emotion_result.intensity})")

# Situation analysis
situation_result = situation_agent.analyze(message)
print(f"Emergency: {situation_result.emergency_category} - {situation_result.severity_level}")
```

#### Audio Analysis

To analyze emergency messages with audio:

```python
# Analyze with audio file
emotion_result = emotion_agent.analyze(
    message="Help me please!",
    audio_path="path/to/audio.wav",
    timestamp=5.0  # 5 seconds into the call
)
```

## 📁 Project Structure

```
langchain_voice_agent/
├── agents/                     # AI agent implementations
│   ├── __init__.py
│   ├── emotion_agent.py       # Emotion analysis agent
│   └── situation_agent.py     # Situation assessment agent
├── models/                     # Pydantic data models
│   ├── __init__.py
│   ├── context.py             # Context entry models
│   ├── emotion.py             # Emotion-related models
│   └── situation.py           # Situation-related models
├── tools/                      # Analysis tools and utilities
│   ├── __init__.py
│   ├── context_management.py  # Context/session management
│   └── emotion_tool.py        # Audio & emotion analysis tools
├── context_data/              # Session data storage (JSON files)
├── test/                      # Unit tests
│   ├── __init__.py
│   └── test_emotion.py
├── config.py                  # Configuration and environment setup
├── main.py                    # Main entry point and CLI
├── langgraph.json            # LangGraph configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key (required) | None |
| `MODEL_NAME` | Gemini model to use | `gemini-1.5-flash` |

### Context Data Directory

Session data is stored in `./context_data/` as JSON files. Each session has a unique ID and contains:
- Emotion analysis results
- Situation assessment results
- Temporal emotion history
- Timestamps and metadata

## 🔧 Development Status & Roadmap

### ✅ Current Features
- [x] Text-based emotion analysis
- [x] Audio emotion analysis with librosa
- [x] Situation assessment
- [x] LangGraph workflow orchestration
- [x] Context management
- [x] CLI interface
- [x] Session persistence
- [x] Cross-modal validation
- [x] Temporal emotion tracking

### 🚧 In Progress
- [ ] Real-time audio streaming support
- [ ] Enhanced audio processing models
- [ ] Web UI for emergency operators
- [ ] Multi-language support
- [ ] Integration with emergency dispatch systems

### 📅 Planned Features
- [ ] Voice activity detection
- [ ] Automatic emergency routing
- [ ] Historical analysis and reporting
- [ ] Multi-agent collaboration
- [ ] REST API with FastAPI
- [ ] Docker containerization
- [ ] Comprehensive test coverage
- [ ] Performance optimization
- [ ] Production deployment guides

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest test/

# Run with coverage
python -m pytest test/ --cov=. --cov-report=html

# Run specific test file
python -m pytest test/test_emotion.py -v
```

## 🤝 Contributing

Contributions are welcome! This project is in active development, and we appreciate any help.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Add unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system is designed as a **supplementary tool** for emergency response analysis and should not be used as the sole basis for emergency decisions. Always follow established emergency protocols and defer to trained professionals.

**Important Notes:**
- This software is under active development and not production-ready
- Emotion and situation analysis may not always be accurate
- Do not rely solely on AI analysis for critical emergency decisions
- Always verify AI recommendations with human judgment
- Test thoroughly before using in any real-world scenario

## 📚 Dependencies

Key libraries used in this project:

- **LangChain** - Framework for building LLM applications
- **LangGraph** - Library for building stateful multi-agent workflows
- **Google Generative AI** - Gemini AI models for analysis
- **Pydantic** - Data validation and settings management
- **librosa** - Audio analysis and feature extraction
- **FastAPI** - Web framework for API endpoints (planned)
- **pytest** - Testing framework

## 🐛 Known Issues

- Audio analysis requires `.wav` or `.mp3` format
- Some edge cases in cross-modal validation need refinement
- Temporal trend analysis requires at least 2 emotion entries
- Large audio files may cause memory issues

## 💬 Support & Contact

- **Issues**: Please report bugs and request features via [GitHub Issues](https://github.com/yourusername/langchain_voice_agent/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/yourusername/langchain_voice_agent/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Audio processing with [librosa](https://librosa.org/)

---

**⚡ Status**: Under Active Development | **Last Updated**: October 2025

*Star this repository if you find it useful! ⭐*

