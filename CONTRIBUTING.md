# Contributing to LangChain Voice Agent

Thank you for your interest in contributing to the LangChain Voice Agent project! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Google API key for testing
- Basic understanding of LangChain and LangGraph

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/aijurist/Agent-for-Call-Analysis.git
   cd Agent-for-Call-Analysis
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/aijurist/Agent-for-Call-Analysis.git
   ```

4. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Set up your `.env` file with test credentials

## 🔀 Contribution Workflow

### 1. Create a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

### 2. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add comments where necessary
- Update documentation if needed
- Add tests for new functionality

### 3. Test Your Changes

Run the test suite to ensure everything works:

```bash
# Run all tests
python -m pytest test/

# Run with coverage
python -m pytest test/ --cov=. --cov-report=html

# Run specific test
python -m pytest test/test_emotion.py -v
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of your changes"
```

**Good commit messages:**
- `Add audio streaming support for real-time analysis`
- `Fix emotion intensity calculation bug`
- `Update README with installation instructions`
- `Refactor context management for better performance`

**Bad commit messages:**
- `Update`
- `Fix bug`
- `Changes`

### 5. Push Your Changes

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template with:
   - Description of changes
   - Related issues (if any)
   - Testing performed
   - Screenshots (if applicable)

## 📝 Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

Example:
```python
def analyze_emotion(message: str, confidence_threshold: float = 0.7) -> EmotionAnalysisOutput:
    """
    Analyze the emotional content of a message.
    
    Args:
        message: The text message to analyze
        confidence_threshold: Minimum confidence score (0-1)
        
    Returns:
        EmotionAnalysisOutput containing analysis results
    """
    # Implementation here
    pass
```

### Documentation

- Add docstrings to all classes and functions
- Use Google-style docstrings
- Keep README.md up to date
- Document any breaking changes

### Testing

- Write unit tests for new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_emotion_analysis_with_high_intensity_panic():
    """Test that panic emotion is correctly identified with high intensity."""
    # Test implementation
    pass
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: 
   - Python version
   - Operating system
   - Relevant library versions
6. **Error Messages**: Full error traceback if applicable
7. **Screenshots**: If relevant

Use the bug report template when creating an issue.

## 💡 Feature Requests

When requesting features:

1. Check if the feature already exists or is planned
2. Clearly describe the feature and its use case
3. Explain why it would be valuable
4. Provide examples if possible

## 🔍 Code Review Process

All contributions go through code review:

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Peer Review**: At least one maintainer reviews the code
3. **Feedback**: Reviewers may request changes
4. **Approval**: Once approved, the PR is merged

### Review Criteria

- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations
- Security implications

## 🏷️ Areas for Contribution

### High Priority

- [ ] Real-time audio streaming support
- [ ] Enhanced audio processing models
- [ ] Web UI for operators
- [ ] Multi-language support
- [ ] Comprehensive test coverage

### Medium Priority

- [ ] Performance optimization
- [ ] Better error handling
- [ ] Additional emotion categories
- [ ] Integration examples
- [ ] Docker containerization

### Good First Issues

Look for issues tagged with `good-first-issue`:
- Documentation improvements
- Adding examples
- Writing tests
- Small bug fixes

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Testing with pytest](https://docs.pytest.org/)

## 🤝 Community Guidelines

- Be respectful and constructive
- Help others when possible
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Keep discussions on-topic

## ❓ Questions?

- Open a [Discussion](https://github.com/ORIGINAL_OWNER/langchain_voice_agent/discussions)
- Check existing issues and PRs
- Reach out to maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LangChain Voice Agent! 🎉

