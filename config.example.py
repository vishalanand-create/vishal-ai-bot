# Configuration file for Agent Vish
# Copy this file to config.py and fill in your actual values

# API Keys
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
BOT_TOKEN = "your_bot_token_here"

# AI Model API Keys
OPENAI_API_KEY = "your_openai_api_key_here"  # ChatGPT Pro
GOOGLE_API_KEY = "your_google_api_key_here"  # Gemini Pro
PERPLEXITY_API_KEY = "your_perplexity_api_key_here"  # Perplexity Pro

# Bot Configuration
BOT_NAME = "Agent Vish"
BOT_PREFIX = "!"
MAX_MESSAGE_LENGTH = 2000

# Database Configuration
DATABASE_URL = "sqlite:///bot_database.db"
# or for PostgreSQL: "postgresql://user:password@localhost/dbname"

# Logging Configuration
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "bot.log"

# Optional Features
ENABLE_ANALYTICS = False
ENABLE_AUTO_RESPONSES = True
RESPONSE_TIMEOUT = 30  # seconds

# Admin Settings
ADMIN_USER_IDS = []  # Add admin user IDs here
ALLOWED_CHANNELS = []  # Add allowed channel IDs here (empty list = all channels)
