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
- **Data Analysis API**: Process CSV/Excel reports with automated analysis and recommendations

## Installation
### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Step-by-Step Installation
1. Clone the repository:
```
bash
git clone https://github.com/vishalanand-create/vishal-ai-bot.git
cd vishal-ai-bot
```
2. Create a virtual environment (recommended):
```
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install required dependencies:
```
bash
pip install -r requirements.txt
```
4. Set up configuration:
- Copy the example configuration file
- Add your API keys and customize settings as needed
```
bash
cp config.example.py config.py
# Edit config.py with your settings
```

## Quick Start
### Basic Usage
```
python
from agent_vish import AgenticAIBot, greet_skill, faq_skill, about_me_skill

bot = AgenticAIBot()
bot.add_skill(greet_skill)
bot.add_skill(faq_skill)
bot.add_skill(about_me_skill)

print(bot.receive_message("hello"))
```

## Analytics Skill (New)
The analytics_skill enables friendly responses to queries related to Google Analytics, Google Sheets, and MyOperator stats. It currently uses stubbed API calls to illustrate the live integration potential.

Supported triggers:
- "google analytics"
- "google sheets"
- "myoperator" or "myoperator stats"

How it works:
- On matching a trigger, the skill returns a helpful message describing what live integration could provide, along with a small sample stub of data.
- No real API calls are made yet—this is a safe preview of the integration.

### Registering the skill
The skill is automatically registered in the bot initialization in `agent_vish.py`. If you are wiring it manually, add:
```
python
from skills.analytics_skill import analytics_skill
bot.add_skill(lambda msg, mem: analytics_skill(msg))
```

### Examples
```
python
from agent_vish import AgenticAIBot
from skills.analytics_skill import analytics_skill

bot = AgenticAIBot()
bot.add_skill(lambda msg, mem: analytics_skill(msg))

print(bot.receive_message("Show me google analytics"))
print(bot.receive_message("Connect to google sheets"))
print(bot.receive_message("myoperator stats for today"))
```

Expected responses are friendly, include sample data, and suggest enabling live integration.

## Report Analysis Skill
The `report_skill` analyzes table-like data placed in `memory['report_data']` and summarizes stats, numeric columns, and missing data.

### Example
```
python
from agent_vish import AgenticAIBot, report_skill

bot = AgenticAIBot()
bot.add_skill(report_skill)

bot.memory['report_data'] = [
    {"region": "East", "sales": 120.5, "units": 10},
    {"region": "West", "sales": 99.0, "units": 8},
]

print(bot.receive_message("summarize report"))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
