# Changelog

All notable changes to the LangChain Voice Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Real-time audio streaming support
- Web UI for emergency operators
- Multi-language support
- REST API with FastAPI
- Docker containerization
- Enhanced audio processing models
- Automatic emergency routing
- Historical analysis and reporting
- Integration with emergency dispatch systems

## [0.1.0] - 2025-10-22

### Added - Initial Release

#### Core Features
- **Emotion Analysis Agent**
  - Text-based emotion detection (fear, anger, sadness, distress, panic, confusion)
  - Audio emotion analysis using librosa
  - Emotion intensity assessment (low, medium, high, extreme)
  - Confidence scoring for analysis results
  - Urgency detection

- **Situation Assessment Agent**
  - Emergency categorization (medical, fire, crime, traffic, disaster, etc.)
  - Severity level detection (low to life-threatening)
  - Key detail extraction from messages
  - Recommended action generation
  - Required resource identification

- **Audio Processing**
  - Audio feature extraction (pitch, volume, speech rate, prosody)
  - Audio emotion classification
  - Support for WAV and MP3 formats
  - Cross-modal validation between text and audio

- **Advanced Analysis Tools**
  - Temporal emotion tracking over time
  - Emotion trend analysis (escalating, de-escalating, stable)
  - Cross-modal validation between text and audio analyses
  - Emotion lexicon scoring for quick validation

- **Workflow Orchestration**
  - LangGraph-based multi-agent workflow
  - Sequential analysis pipeline (emotion → situation → aggregation)
  - Context management and sharing between agents
  - Session-based data persistence

- **User Interfaces**
  - Interactive CLI for emergency message analysis
  - LangGraph server mode for API access
  - Programmatic API for integration

#### Infrastructure
- Pydantic models for type safety and validation
- Google Gemini AI integration (gemini-1.5-flash)
- JSON-based session storage in `context_data/`
- Comprehensive error handling and logging
- Environment-based configuration

#### Documentation
- Comprehensive README with architecture diagrams
- Installation and setup instructions
- Usage examples and code samples
- Contributing guidelines
- MIT License
- Changelog

#### Testing
- Unit tests for emotion analysis
- Test fixtures and sample data

### Technical Details

#### Dependencies
- LangChain 0.3.21 (LLM application framework)
- LangGraph 0.3.21 (workflow orchestration)
- Google Generative AI 2.1.2 (Gemini models)
- librosa 0.10.2 (audio processing)
- Pydantic 2.11.1 (data validation)
- FastAPI 0.115.12 (web framework foundation)

#### Models
- `EmotionType`: Enum for emotion categories
- `EmotionIntensity`: Enum for intensity levels
- `EmotionAnalysisOutput`: Structured emotion analysis results
- `AudioFeatures`: Audio signal features
- `AudioEmotionOutput`: Audio-based emotion results
- `TemporalEmotionOutput`: Time-series emotion data
- `CrossModalValidationOutput`: Multi-modal consistency check
- `SituationAnalysisOutput`: Emergency situation assessment
- `EmergencyCategory`: Enum for emergency types
- `SeverityLevel`: Enum for severity assessment

#### Agents
- `EmotionAnalyzerAgent`: Analyzes emotional content
- `SituationAnalyzerAgent`: Assesses emergency situations

#### Tools
- `AudioFeatureExtractorTool`: Extracts audio features
- `AudioEmotionClassifierTool`: Classifies emotions from audio
- `EmotionLexiconScorerTool`: Quick lexicon-based scoring
- `TemporalEmotionAnalyzerTool`: Tracks emotions over time
- `CrossModalValidatorTool`: Validates text vs audio consistency
- `ContextManagementTool`: Manages session context

### Known Issues
- Audio files must be in WAV or MP3 format
- Large audio files may cause memory issues
- Temporal trend analysis requires at least 2 emotion entries
- Some edge cases in cross-modal validation need refinement

### Security Notes
- API keys must be stored in `.env` file (not in version control)
- Session data stored locally in JSON format
- No authentication/authorization system yet (planned for future)

---

## Development Notes

### Version Numbering
- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Process
1. Update version in `__init__.py` files
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
4. Push tag: `git push origin v0.1.0`

### Contributors
Thank you to all contributors who helped with this initial release!

---

[Unreleased]: https://github.com/OWNER/langchain_voice_agent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/OWNER/langchain_voice_agent/releases/tag/v0.1.0

