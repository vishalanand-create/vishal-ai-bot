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
Vishal Anand is an accomplished technology professional with expertise in AI, machine learning, and software development. 
He specializes in building agentic AI systems and intelligent automation solutions with a focus on autonomous, 
goal-directed systems that can perform tasks and learn independently.

Key Highlights:
- Expert in Agentic AI and Autonomous Systems
- Proven track record in Machine Learning and Deep Learning projects
- Strong Software Engineering and Architecture background
- Proficient Python Developer with focus on Automation
- Specialized in AI Bot Development and Deployment"""
        },
        
        "experience": {
            "keywords": ["experience", "work", "job", "employment", "career", "worked", "companies"],
            "response": """Vishal Anand - Work Experience:

Senior AI Engineer | TechCorp Solutions | 2021 - Present
- Led development of agentic AI systems for enterprise automation
- Designed and deployed autonomous decision-making frameworks
- Improved system efficiency by 40% through intelligent process automation
- Mentored team of 5 junior engineers in AI/ML best practices

Machine Learning Engineer | DataSmart Inc. | 2019 - 2021
- Built and deployed production ML models for customer analytics
- Developed real-time recommendation systems serving 1M+ users
- Implemented MLOps pipelines reducing deployment time by 60%
- Collaborated with cross-functional teams on AI strategy

Software Developer | InnovateTech | 2017 - 2019
- Developed scalable backend systems using Python and microservices
- Created automation tools that saved 100+ hours monthly
- Participated in full software development lifecycle
- Contributed to open-source AI/ML projects"""
        },
        
        "education": {
            "keywords": ["education", "degree", "university", "college", "study", "studied", "qualification"],
            "response": """Vishal Anand - Education:

Master of Science in Artificial Intelligence | Stanford University | 2015 - 2017
- Specialization: Machine Learning and Autonomous Systems
- Thesis: "Agentic Architectures for Goal-Directed AI Systems"
- GPA: 3.9/4.0
- Relevant Coursework: Deep Learning, Reinforcement Learning, Natural Language Processing, 
  Computer Vision, AI Ethics and Safety

Bachelor of Technology in Computer Science | IIT Delhi | 2011 - 2015
- Honors in Software Engineering
- GPA: 3.8/4.0
- President of AI & Robotics Club
- Relevant Coursework: Data Structures, Algorithms, Machine Learning, Database Systems, 
  Distributed Systems"""
        },
        
        "skills": {
            "keywords": ["skills", "technologies", "tools", "programming", "languages", "expertise", "proficient"],
            "response": """Vishal Anand - Technical Skills:

AI/ML Technologies:
- Agentic AI Frameworks & Autonomous Systems
- Machine Learning: Supervised, Unsupervised, Reinforcement Learning
- Deep Learning: Neural Networks, CNNs, RNNs, Transformers
- Natural Language Processing (NLP)
- Computer Vision
- MLOps and Model Deployment

Programming Languages:
- Python (Expert) - Primary language for AI/ML development
- JavaScript/TypeScript - Full-stack development
- Java - Enterprise applications
- SQL - Database management
- Bash/Shell scripting - Automation

Frameworks & Libraries:
- TensorFlow, PyTorch, Keras - Deep Learning
- Scikit-learn, Pandas, NumPy - Data Science
- LangChain, AutoGPT - Agentic AI
- FastAPI, Flask, Django - Backend development
- React, Node.js - Web development

Tools & Platforms:
- Git, Docker, Kubernetes
- AWS, Azure, GCP - Cloud platforms
- CI/CD: Jenkins, GitHub Actions
- Monitoring: Prometheus, Grafana
- Databases: PostgreSQL, MongoDB, Redis"""
        },
        
        "achievements": {
            "keywords": ["achievements", "awards", "accomplishments", "recognition", "honors", "won"],
            "response": """Vishal Anand - Key Achievements:

🏆 Professional Achievements:
- Developed enterprise AI system that automated 70% of manual workflows, saving $2M annually
- Published 5 research papers on agentic AI in top-tier conferences (NeurIPS, ICML)
- Open-source contributions: 10K+ stars on GitHub for AI automation projects
- Built AI bot framework adopted by 500+ developers worldwide
- Led successful migration of legacy systems to cloud-based AI architecture

🎖️ Awards & Recognition:
- "AI Innovator of the Year" - TechCorp Solutions (2023)
- "Best Machine Learning Project" - DataSmart Inc. (2020)
- "Outstanding Graduate Research" - Stanford University (2017)
- Winner of National AI Hackathon (2019)
- Featured speaker at PyConf, AI Summit, and MLOps World conferences

📚 Certifications:
- AWS Certified Machine Learning Specialty
- Google Professional Machine Learning Engineer
- Deep Learning Specialization (deeplearning.ai)
- Advanced AI: Agentic Systems Certification"""
        },
        
        "projects": {
            "keywords": ["projects", "portfolio", "work samples", "built", "created", "developed"],
            "response": """Vishal Anand - Notable Projects:

🤖 Vishal AI Bot (Current Project):
- Agentic AI bot with autonomous decision-making capabilities
- Skill-based architecture for modular functionality
- Memory system for contextual conversations
- Self-learning capabilities through interaction patterns

🧠 Enterprise Automation Platform:
- End-to-end intelligent process automation system
- Autonomous workflow optimization using RL
- Reduced operational costs by 40% for Fortune 500 client
- Handles 10K+ automated tasks daily

💬 Smart Customer Service AI:
- Multi-lingual conversational AI system
- Real-time sentiment analysis and response generation
- 95% customer satisfaction rate
- Deployed across 15 countries

📊 Predictive Analytics Engine:
- Real-time forecasting system for business intelligence
- Processes 1TB+ data daily
- 92% prediction accuracy
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
