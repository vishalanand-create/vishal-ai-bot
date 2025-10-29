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

# Start conversation
response = bot.chat("Hello!")
print(response)
```

## API Endpoints

Agent Vish provides a Flask-based REST API for integration with external applications.

### Starting the API Server

```bash
python api.py
```

The server will start on `http://localhost:5000` by default.

### Available Endpoints

#### 1. Chat Endpoint

**URL:** `/chat`  
**Method:** `POST`  
**Description:** Interact with Agent Vish via text messages

**Request Body:**
```json
{
  "message": "Hello, Agent Vish!"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Hello, Agent Vish!",
  "response": "Agent Vish received: Hello, Agent Vish!"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Agent Vish!"}'
```

#### 2. Report Summarization Endpoint

**URL:** `/api/summarize_report`  
**Method:** `POST`  
**Description:** Upload CSV or Excel files for automated data analysis, statistical summary, and AI-generated recommendations

**Request:**
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file` (required): CSV or Excel file (.csv, .xlsx, .xls)

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_rows": 1000,
    "total_columns": 5,
    "columns": ["column1", "column2", "column3", "column4", "column5"],
    "column_types": {
      "column1": "int64",
      "column2": "float64",
      "column3": "object"
    },
    "missing_values": {
      "column1": 0,
      "column2": 5,
      "column3": 2
    },
    "total_missing_values": 7,
    "numeric_columns": ["column1", "column2"],
    "numeric_column_count": 2,
    "categorical_columns": ["column3"],
    "categorical_column_count": 1,
    "duplicate_rows": 3,
    "statistics": {
      "column1": {
        "count": 1000,
        "mean": 50.5,
        "std": 15.2,
        "min": 10,
        "25%": 35,
        "50%": 50,
        "75%": 65,
        "max": 100
      }
    },
    "strong_correlations": [
      {
        "column1": "column1",
        "column2": "column2",
        "correlation": 0.85
      }
    ],
    "unique_value_counts": {
      "column3": 50
    },
    "memory_usage_mb": 0.5
  },
  "recommendations": [
    "Dataset has 7 missing values (0.1%). Review data collection process.",
    "Found 3 duplicate rows (0.3%). Consider deduplication to improve data quality.",
    "Dataset contains 2 numeric column(s). Consider statistical analysis, trend analysis, and predictive modeling.",
    "Found 1 strong correlation(s) between numeric variables. Review for potential multicollinearity in predictive models.",
    "Dataset has 1 categorical column(s). Consider encoding strategies for machine learning applications.",
    "Consider creating visualizations: scatter plots, correlation heatmaps, and distribution plots for deeper insights.",
    "Mixed data types present. Consider segmentation analysis and group comparisons for meaningful insights."
  ]
}
```

**Example with cURL:**
```bash
curl -X POST http://localhost:5000/api/summarize_report \
  -F "file=@/path/to/your/report.csv"
```

**Example with Python:**
```python
import requests

url = "http://localhost:5000/api/summarize_report"
files = {"file": open("report.csv", "rb")}

response = requests.post(url, files=files)
result = response.json()

print("Summary:", result["summary"])
print("Recommendations:", result["recommendations"])
```

**Error Responses:**

- **400 Bad Request:** Missing or invalid file
```json
{
  "status": "error",
  "error": "No file provided. Please upload a CSV or Excel file."
}
```

- **400 Bad Request:** Unsupported file format
```json
{
  "status": "error",
  "error": "Unsupported file format: .txt. Please upload CSV or Excel files."
}
```

- **500 Internal Server Error:** Processing error
```json
{
  "status": "error",
  "error": "An unexpected error occurred: [error details]"
}
```

**Features:**
- Comprehensive statistical analysis of numeric columns
- Correlation detection for multicollinearity assessment
- Missing value and duplicate detection
- Categorical variable analysis with cardinality assessment
- Outlier detection using IQR method
- Memory usage analysis
- Automated, actionable recommendations based on data characteristics
- Support for both CSV and Excel formats (.csv, .xlsx, .xls)

## Skills System

### Core Skills

Agent Vish includes the following built-in skills:

1. **greet_skill**: Handles greetings and welcomes users
2. **faq_skill**: Answers frequently asked questions
3. **report_skill**: Processes and analyzes CSV/Excel data files

### Creating Custom Skills

You can easily extend Agent Vish by creating custom skills:

```python
def custom_skill(user_input):
    """
    Custom skill example
    """
    if "custom" in user_input.lower():
        return "This is a custom response!"
    return None

# Add to bot
bot.add_skill(custom_skill)
```

## Architecture

Agent Vish follows a modular architecture:

```
vishal-ai-bot/
├── agent_vish.py       # Main bot logic and agentic framework
├── api.py              # Flask API endpoints
├── skills/             # Modular skills directory
│   └── core_skills.py  # Core skill implementations
├── config.py           # Configuration settings
└── requirements.txt    # Python dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Vishal Anand

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
