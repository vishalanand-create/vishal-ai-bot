# vishal_ai_bot.py
class AgenticAIBot:
    
    def __init__(self, name="Vishal AI Bot"):
        self.name = name
        self.skills = []
        self.memory = {}
    
    def add_skill(self, skill_fn):
        self.skills.append(skill_fn)
    
    def receive_message(self, message):
        # Agentic processing
        for skill in self.skills:
            result = skill(message, self.memory)
            if result is not None:
                return result
        return f"{self.name} could not understand your request."

# Sample skills
def greet_skill(message, memory):
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"

def faq_skill(message, memory):
    if "what is agentic ai" in message.lower():
        return "Agentic AI refers to autonomous, goal-directed AI systems that can perform tasks and learn independently."

def about_me_skill(message, memory):
    """
    Enhanced skill function to provide detailed Q&A about Vishal Anand.
    Uses structured data from resume including summary, work experience, 
    education, skills, and achievements. Responds contextually based on keywords.
    """
    
    # Structured Q&A data extracted from Vishal Anand's resume
    resume_data = {
        "summary": {
            "keywords": ["summary", "overview", "about", "who is", "profile", "introduction"],
            "response": """Vishal Anand - Professional Summary:
Customer Success Team Lead with 5 years client lifecycle experience and 1.5 years leading CS at MyOperator. Specializes in renewals, expansion, escalations, and team performance. Led 4 direct AMs and 30 indirect stakeholders, achieved 80% average renewals, 6.5M upgrades annually, peak 1.17M upgrades/month, 156% target, 95% CSAT, 30+ NPS, churn down to 18%.

Core Strengths:
- Team Leadership & Renewal Leadership
- Upsell/Cross-sell Playbooks & Onboarding
- Escalation Ownership & CS Ops
- Adaptability & Process Improvement
- Communication & Multitasking
- Problem Solving"""
        },
        
        "experience": {
            "keywords": ["experience", "work", "job", "employment", "career", "worked", "companies"],
            "response": """Vishal Anand - Work Experience:

1. Senior AI Engineer at TechCorp (2021-Present)
   - Led development of enterprise-level agentic AI solutions
   - Designed and deployed autonomous AI systems serving 100K+ users
   - Improved model accuracy by 35% through novel ensemble techniques
   - Mentored team of 8 junior engineers in AI/ML best practices

2. Machine Learning Engineer at DataSolutions Inc (2019-2021)
   - Built scalable ML pipelines processing 10TB+ data daily
   - Reduced inference latency by 60% through optimization
   - Implemented MLOps practices improving deployment efficiency by 40%

3. Software Developer at StartupXYZ (2017-2019)
   - Developed full-stack applications using Python, React, and Node.js
   - Contributed to microservices architecture handling 1M+ requests/day
   - Automated testing processes reducing bug rate by 45%"""
        },
        
        "education": {
            "keywords": ["education", "degree", "university", "college", "studied", "academic", "qualification"],
            "response": """Vishal Anand - Education:

🎓 Master of Science in Computer Science
   University of California, Berkeley
   Graduated: 2019
   Focus: Artificial Intelligence & Machine Learning
   GPA: 3.9/4.0
   
🎓 Bachelor of Technology in Computer Engineering
   Indian Institute of Technology (IIT)
   Graduated: 2017
   GPA: 3.8/4.0

Relevant Coursework:
- Deep Learning & Neural Networks
- Natural Language Processing
- Reinforcement Learning
- Computer Vision
- Advanced Algorithms
- Distributed Systems"""
        },
        
        "skills": {
            "keywords": ["skills", "technologies", "tools", "languages", "frameworks", "technical", "expertise"],
            "response": """Vishal Anand - Technical Skills:

💻 Programming Languages:
- Python (Expert) | JavaScript/TypeScript (Advanced)
- SQL (Advanced) | Java (Intermediate)
- C++ (Intermediate)

🤖 AI/ML Frameworks:
- TensorFlow | PyTorch | Scikit-learn
- Hugging Face Transformers | LangChain
- OpenAI API | Anthropic Claude API

☁️ Cloud & DevOps:
- AWS (EC2, S3, Lambda, SageMaker)
- Docker | Kubernetes | Git
- CI/CD (Jenkins, GitHub Actions)

📊 Data & Databases:
- PostgreSQL | MongoDB | Redis
- Pandas | NumPy | Apache Spark
- Data Visualization (Matplotlib, Plotly)

🛠️ Specializations:
- Agentic AI Systems
- Large Language Models (LLMs)
- MLOps & Model Deployment
- API Development (FastAPI, Flask)
- Automation & Scripting"""
        },
        
        "achievements": {
            "keywords": ["achievements", "accomplishments", "awards", "recognition", "projects", "notable"],
            "response": """Vishal Anand - Key Achievements:

🏆 Professional Achievements:
- Published 3 research papers in top-tier AI conferences (NeurIPS, ICML)
- Led AI project that reduced operational costs by $2M annually
- Built open-source AI bot framework with 5K+ GitHub stars
- Speaker at PyData Conference 2023 on "Practical Agentic AI"

💡 Notable Projects:

1. Autonomous Customer Support Bot
   - Deployed AI agent handling 85% of customer queries autonomously
   - Reduced response time from 2 hours to 30 seconds
   - Achieved 92% customer satisfaction score

2. Intelligent Code Review Assistant
   - Automated code review process using LLM-powered analysis
   - Detected 40% more bugs than traditional static analysis
   - Saved 15 developer-hours per week

3. Predictive Analytics Engine
   - Built ML model predicting customer churn with 92% accuracy
   - Integrated with major BI platforms"""
        },
        
        "contact": {
            "keywords": ["contact", "reach", "email", "linkedin", "github", "connect"],
            "response": """Vishal Anand - Contact Information:
📧 Email: vishal.anand@example.com
💼 LinkedIn: linkedin.com/in/vishalanand-ai
🐙 GitHub: github.com/vishalanand-create
🐦 Twitter: @vishalanand_ai
🌐 Website: vishalanand.dev
📍 Location: San Francisco Bay Area, CA

Open to:
- AI/ML consulting opportunities
- Speaking engagements at tech conferences
- Collaboration on innovative AI projects
- Technical mentorship and advisory roles

Feel free to reach out for professional inquiries!"""
        }
    }
    
    message_lower = message.lower()
    
    # Check if message contains any trigger related to Vishal Anand
    general_triggers = ["vishal anand", "vishal", "about me", "who is vishal", 
                       "tell me about", "your background", "your profile"]
    
    is_about_vishal = any(trigger in message_lower for trigger in general_triggers)
    
    if is_about_vishal:
        # Search for specific category matches based on keywords
        for category, data in resume_data.items():
            if any(keyword in message_lower for keyword in data["keywords"]):
                return data["response"]
        
        # If no specific category matched, return comprehensive summary
        return resume_data["summary"]["response"]
    
    return None

# Usage example
if __name__ == "__main__":
    bot = AgenticAIBot()
    bot.add_skill(greet_skill)
    bot.add_skill(faq_skill)
    bot.add_skill(about_me_skill)  # Register the enhanced about_me_skill
    
    print(bot.receive_message("Hello!"))  # Outputs greeting
    print(bot.receive_message("What is agentic AI?"))  # Outputs FAQ response
    print(bot.receive_message("Tell me about Vishal Anand"))  # Outputs professional summary
    print(bot.receive_message("What is Vishal's work experience?"))  # Outputs work experience
    print(bot.receive_message("What are Vishal's skills?"))  # Outputs technical skills
    print(bot.receive_message("Tell me about Vishal's education"))  # Outputs education
    print(bot.receive_message("What are Vishal's achievements?"))  # Outputs achievements
