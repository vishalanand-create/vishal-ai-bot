# agent-vish

## Introduction

Agent Vish is an intelligent agentic AI assistant built with Python, featuring modular skills architecture and persistent memory capabilities. This bot implements sophisticated agentic decision flows, enabling it to autonomously handle complex tasks, make contextual decisions, and maintain conversation history across sessions.

## Key Features

- **Agentic Decision Making**: Advanced AI agent that can autonomously plan and execute multi-step tasks
- **Modular Skills System**: Extensible architecture allowing easy addition of new capabilities
- **Persistent Memory**: Maintains context and learns from past interactions
- **Python-Based**: Built with modern Python practices for reliability and maintainability
- **Flexible Integration**: Designed to work with various AI models and APIs
- **Customizable Behavior**: Easy configuration to adapt the bot to specific use cases

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Step-by-Step Installation

1. Clone the repository:
```bash
git clone https://github.com/vishalanand-create/vishal-ai-bot.git
cd vishal-ai-bot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
- Copy the example configuration file
- Add your API keys and customize settings as needed
```bash
cp config.example.py config.py
# Edit config.py with your settings
```

## Quick Start

### Basic Usage

```python
from agent_vish import AgenticAIBot, greet_skill, faq_skill, about_me_skill

# Initialize Agent Vish
bot = AgenticAIBot(name="Agent Vish")

# Add skills
bot.add_skill(greet_skill)
bot.add_skill(faq_skill)
bot.add_skill(about_me_skill)

# Interact with the bot
response = bot.receive_message("Hello!")
print(response)
```

### Advanced Usage

#### Creating Custom Skills

```python
def custom_skill(message, memory):
    """Your custom skill implementation"""
    if "specific_keyword" in message.lower():
        return "Custom response"
    return None

bot.add_skill(custom_skill)
```

#### Using Memory

Agent Vish maintains conversation context through its memory system:

```python
# Memory is automatically managed
bot.memory['user_preference'] = 'value'
# Skills can access and modify memory
```

## Project Structure

```
agent-vish/
├── agent_vish.py          # Main bot implementation
├── requirements.txt       # Project dependencies
├── config.py             # Configuration file (create from config.example.py)
├── config.example.py     # Example configuration
├── README.md             # This file
├── tests/                # Test suite
│   ├── test_bot.py
│   └── test_skills.py
└── docs/                 # Additional documentation
    ├── architecture.md
    ├── skills_guide.md
    └── api_reference.md
```

## Core Components

### AgenticAIBot Class

The main class that orchestrates the bot's functionality:

- **Initialization**: Sets up the bot with a name and empty skills/memory
- **Skill Management**: Add and manage modular skills
- **Message Processing**: Routes messages through skills for agentic decision making
- **Memory Management**: Maintains persistent context across interactions

### Skills System

Skills are modular functions that process messages and return responses:

```python
def skill_template(message, memory):
    # Process message
    # Access/modify memory if needed
    # Return response or None
    return response_or_none
```

## Configuration

Agent Vish can be configured through the `config.py` file:

```python
# config.py example
BOT_NAME = "Agent Vish"
API_KEYS = {
    'openai': 'your-api-key',
    # Add other API keys as needed
}
MEMORY_PERSISTENCE = True
LOG_LEVEL = 'INFO'
```

## Available Skills

### Built-in Skills

1. **greet_skill**: Handles greeting messages
2. **faq_skill**: Answers frequently asked questions about agentic AI
3. **about_me_skill**: Provides detailed information about Vishal Anand
   - Handles questions about team leadership challenges
   - Provides insights on handling escalations
   - Shares leadership philosophy
   - Discusses upsell and cross-sell strategies

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run with coverage:

```bash
python -m pytest --cov=agent_vish tests/
```

## Development

### Setting Up Development Environment

1. Clone the repository
2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```
3. Set up pre-commit hooks:
```bash
pre-commit install
```

### Code Style

This project follows PEP 8 style guidelines:

```bash
# Format code
black agent_vish.py

# Lint code
flake8 agent_vish.py
```

## Deployment

### Local Deployment

```bash
python agent_vish.py
```

### Docker Deployment

```bash
# Build image
docker build -t agent-vish .

# Run container
docker run -d -p 8000:8000 agent-vish
```

### Cloud Deployment

Agent Vish can be deployed to various cloud platforms:

- **AWS Lambda**: Serverless deployment
- **Google Cloud Run**: Containerized deployment
- **Azure Functions**: Serverless deployment
- **Heroku**: Platform-as-a-Service deployment

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

2. **Memory Issues**: Clear the memory cache if needed
```python
bot.memory.clear()
```

3. **Skill Not Responding**: Check skill order and return values

## Roadmap

- [ ] Add more sophisticated NLP capabilities
- [ ] Implement multi-language support
- [ ] Add voice interaction capabilities
- [ ] Develop GUI interface
- [ ] Create plugin marketplace
- [ ] Add integration with popular APIs
- [ ] Implement advanced learning mechanisms

## Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- **Code Quality**: Follow PEP 8 and include tests
- **Documentation**: Update documentation to reflect any changes
- **Commit Messages**: Use clear, descriptive commit messages
- **Issue First**: For major changes, open an issue first to discuss the proposed changes

### Areas for Contribution

- Adding new skills and capabilities
- Improving memory management
- Enhancing decision-making algorithms
- Bug fixes and performance improvements
- Documentation improvements
- Test coverage expansion

## Contact Information

- **Repository Owner**: Vishal Anand
- **GitHub**: [@vishalanand-create](https://github.com/vishalanand-create)
- **Project Repository**: [vishal-ai-bot](https://github.com/vishalanand-create/vishal-ai-bot)

For questions, suggestions, or support:
- Open an [Issue](https://github.com/vishalanand-create/vishal-ai-bot/issues)
- Submit a [Pull Request](https://github.com/vishalanand-create/vishal-ai-bot/pulls)
- Start a [Discussion](https://github.com/vishalanand-create/vishal-ai-bot/discussions)

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to all contributors who help improve this project
- Built with modern Python and AI technologies
- Inspired by the need for flexible, intelligent automation

---

**Note**: This bot is under active development. Features and APIs may change as the project evolves. Check back regularly for updates!
