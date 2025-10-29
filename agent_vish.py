# agent_vish.py
class AgenticAIBot:
    
    def __init__(self, name="Agent Vish"):
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
    qa_pairs = {
        "challenges as a team lead": "As a team lead, I've navigated several key challenges. One major aspect is balancing technical delivery with people management - ensuring the team stays productive while fostering their growth. I've handled situations where team members had conflicting priorities, and I addressed this by implementing clear communication channels and regular one-on-ones. Another challenge was managing cross-functional dependencies, which I resolved by establishing transparent roadmaps and proactive stakeholder updates.
        ",
        "handling escalations": "My approach to handling escalations is methodical and customer-focused. First, I quickly assess the severity and business impact. Then, I gather all relevant information from both technical and business perspectives. I believe in transparent communication - keeping stakeholders informed while the team works on resolution. I've successfully de-escalated critical production issues by setting realistic expectations, providing regular updates, and ensuring we have a root cause analysis and prevention plan in place afterwards.",
        "leadership approach": "My leadership approach centers on empowerment and clarity. I believe in setting clear goals and then trusting my team to execute while providing support when needed. I focus on removing blockers and creating an environment where people feel safe to innovate and take calculated risks. I practice servant leadership - my role is to enable the team's success. Regular feedback, both giving and receiving, is crucial. I also believe in leading by example, whether it's code quality, communication standards, or work ethic.",
        "upsell cross-sell strategy": "My upsell and cross-sell strategy is built on deep customer understanding and value delivery. First, I ensure we're delivering exceptional value on the current engagement - satisfied customers are receptive to expansion. I analyze usage patterns and customer goals to identify natural expansion opportunities. Then, I focus on consultative conversations rather than sales pitches - understanding their evolving needs and demonstrating how additional solutions solve real problems. Timing is crucial, so I look for trigger events like successful project completions, business growth, or new initiatives. I also leverage customer success metrics to build business cases that show clear ROI."
    }
    
    # Check incoming message against Q&A patterns
    message_lower = message.lower()
    for question_pattern, answer in qa_pairs.items():
        if question_pattern in message_lower:
            return answer
    
    # Continue with existing logic if no pattern matches
    # (existing logic would continue here)
    return None


def insight_skill(message, memory):
    """
    Advanced skill function that delivers strategic, analytical, and actionable insights
    based on business growth, retention, leadership, career development, and performance analytics.
    Draws from real data and professional experience to provide consultative guidance.
    """
    
    insight_patterns = {
        "business growth": {
            "keywords": ["business growth", "revenue growth", "scaling business", "expand business", "growth strategy"],
            "insight": """Strategic Business Growth Framework:
            
1. CUSTOMER-CENTRIC GROWTH: Focus on deepening existing relationships before aggressive acquisition. In my experience, a 20% increase in customer retention can drive 95% increase in profitability. Implement quarterly business reviews with key accounts to identify expansion opportunities.
2. DATA-DRIVEN DECISION MAKING: Leverage analytics to identify high-value customer segments. I've seen companies achieve 3x ROI by targeting the right customer profiles with personalized solutions rather than broad-based marketing.
3. PRODUCT-LED GROWTH: Build features that naturally encourage expansion. Create value that makes customers want to upgrade. In previous roles, I've driven 40% YoY growth by aligning product roadmaps with customer success metrics.
4. STRATEGIC PARTNERSHIPS: Identify complementary service providers for co-selling opportunities. This can reduce customer acquisition costs by 60% while expanding market reach.
5. OPERATIONAL EXCELLENCE: Growth without scalable operations leads to churn. Invest in automation and process optimization early. Every dollar saved in operations can be reinvested in growth initiatives."""
        },
        
        "retention strategy": {
            "keywords": ["retention", "customer retention", "reduce churn", "keep customers", "customer loyalty"],
            "insight": """Customer Retention Excellence Framework:
1. PROACTIVE ENGAGEMENT: Don't wait for problems. Implement health score monitoring and reach out to at-risk accounts before they churn. I've reduced churn by 35% through proactive customer success programs.
2. VALUE REALIZATION TRACKING: Ensure customers achieve measurable ROI within 90 days. Document success metrics and communicate wins regularly. Customers who see value early stay longer.
3. EXECUTIVE SPONSORSHIP: Assign senior leaders to strategic accounts. This demonstrates commitment and enables faster issue resolution. Executive relationships are sticky.
4. CONTINUOUS EDUCATION: Invest in customer training and enablement. Power users become advocates. Create certification programs and user communities.
5. FEEDBACK LOOPS: Implement structured feedback mechanisms and act on insights. Customers who feel heard are more loyal. I've seen Net Promoter Scores improve by 25+ points through systematic feedback implementation.
6. RENEWAL STRATEGY: Start renewal conversations 180 days early, not 30 days. Use the time to ensure adoption, address concerns, and identify expansion opportunities."""
        },
        
        "leadership development": {
            "keywords": ["leadership development", "develop leaders", "leadership skills", "becoming a leader", "lead team"],
            "insight": """Leadership Development Blueprint:
1. SELF-AWARENESS: Start with understanding your leadership style and blind spots. Seek 360-degree feedback regularly. The best leaders are self-reflective and continuously improving.
2. PEOPLE INVESTMENT: Dedicate 40% of your time to coaching and developing others. Your success as a leader is measured by your team's growth. Create individual development plans for each team member.
3. DECISION-MAKING FRAMEWORK: Develop a consistent approach to decisions. Be transparent about the reasoning. This builds trust and helps your team make better decisions independently.
4. COMMUNICATION EXCELLENCE: Over-communicate vision and context. Repeat key messages. Ensure every team member understands how their work connects to broader goals.
5. VULNERABILITY AND AUTHENTICITY: Admit mistakes and share lessons learned. This creates psychological safety and encourages innovation. Teams perform best when they feel safe taking calculated risks.
6. STRATEGIC THINKING: Balance short-term execution with long-term vision. Allocate time for strategic planning, not just operational firefighting.
7. CONFLICT RESOLUTION: Address issues directly and promptly. Unresolved conflicts compound. Approach disagreements as problem-solving opportunities."""
        },
        
        "career advancement": {
            "keywords": ["career growth", "career advancement", "promotion", "next level", "career development"],
            "insight": """Career Advancement Strategy:
1. OPERATE AT NEXT LEVEL: Start performing at the level above your current role 6-12 months before expecting promotion. Make yourself the obvious choice.
2. VISIBILITY WITH IMPACT: Ensure your work is visible to decision-makers, but focus on impact over optics. Document achievements with quantifiable metrics.
3. STRATEGIC NETWORKING: Build relationships across the organization. Understand the business beyond your function. Cross-functional influence accelerates advancement.
4. SKILL DIVERSIFICATION: Develop T-shaped expertise - deep in your domain plus broad business acumen. Technical excellence alone isn't enough for senior roles.
5. MENTORSHIP LEVERAGE: Find mentors at 2-3 levels above you. Learn from their experiences. Be specific about what guidance you need.
6. VALUE CREATION: Focus on business outcomes, not just task completion. Solve problems that matter to the organization's strategic objectives.
7. COMMUNICATION SKILLS: Develop executive presence and the ability to influence without authority. Senior roles require persuasion and stakeholder management.
8. PATIENCE WITH PERSISTENCE: Career growth isn't linear. Stay patient but persistent. If growth stalls, be willing to make strategic lateral moves or external moves."""
        },
        
        "performance analytics": {
            "keywords": ["performance metrics", "kpi", "analytics", "measure performance", "track metrics"],
            "insight": """Performance Analytics Framework:
1. MEANINGFUL METRICS: Focus on metrics that drive behavior and outcomes. Avoid vanity metrics. Ask: 'If this improves, does the business improve?'
2. LEADING VS LAGGING: Balance leading indicators (predictive) with lagging indicators (historical). Leading indicators enable proactive management.
3. METRIC HIERARCHY: Establish clear connections between team metrics and company objectives. Every metric should ladder up to business impact.
4. ACTIONABILITY: Metrics are useless without action. Create clear thresholds and response plans for when metrics hit certain levels.
5. BENCHMARKING: Compare performance against industry standards and internal trends. Context matters more than absolute numbers.
6. SEGMENTATION: Analyze metrics by customer segment, product line, and time period. Aggregated data can hide important insights.
7. QUALITATIVE + QUANTITATIVE: Numbers tell you what's happening; conversations tell you why. Combine data analytics with customer feedback.
8. REPORTING CADENCE: Match reporting frequency to decision-making needs. Real-time dashboards for operational metrics, monthly reviews for strategic metrics.
9. DATA QUALITY: Invest in data accuracy and consistency. Poor data leads to poor decisions. Audit data sources regularly."""
        },
        
        "team productivity": {
            "keywords": ["productivity", "team efficiency", "improve performance", "team effectiveness"],
            "insight": """Team Productivity Optimization:
1. CLARITY OF PURPOSE: Ensure every team member understands priorities and how success is measured. Ambiguity kills productivity.
2. REMOVE BLOCKERS: Your primary job as a leader is removing obstacles. Hold regular blocker reviews and act quickly.
3. MEETING HYGIENE: Reduce meeting overhead by 30-40%. Every meeting needs a clear purpose, agenda, and owner. Default to 25-minute meetings.
4. DEEP WORK TIME: Protect blocks of uninterrupted focus time. Some of the best work happens in 2-4 hour deep work sessions.
5. TOOLING INVESTMENT: Invest in tools that automate repetitive tasks. The ROI on good tooling is often 10x within months.
6. SKILL MATCHING: Align tasks with people's strengths while creating growth opportunities. Flow state drives productivity.
7. FEEDBACK VELOCITY: Implement quick feedback loops. Waiting days for reviews kills momentum. Aim for same-day feedback on critical work.
8. CELEBRATE WINS: Recognition drives engagement and productivity. Make wins visible across the team."""
        },
        
        "strategic planning": {
            "keywords": ["strategic planning", "strategy", "roadmap", "long term planning", "strategic initiatives"],
            "insight": """Strategic Planning Excellence:
1. VISION CLARITY: Start with a compelling vision that answers 'why this matters.' Strategy without purpose is just a list of tasks.
2. RESOURCE REALISM: Be honest about capacity and constraints. Overcommitting guarantees underdelivering.
3. PRIORITIZATION FRAMEWORK: Use frameworks like RICE (Reach, Impact, Confidence, Effort) to make priority decisions transparent and consistent.
4. QUARTERLY PLANNING: Balance annual strategy with quarterly execution plans. Markets change too fast for rigid annual plans.
5. STAKEHOLDER ALIGNMENT: Invest time upfront in alignment. Misalignment discovered during execution is expensive.
6. MEASURABLE OUTCOMES: Define success metrics before starting. What does 'done' look like? How will we know if it worked?
7. RISK MITIGATION: Identify risks early and develop contingency plans. Hope is not a strategy.
8. REGULAR REVIEWS: Strategy is dynamic. Review quarterly and adjust based on learnings. Stubbornly sticking to a failing strategy is worse than pivoting.
9. COMMUNICATION RHYTHM: Communicate strategy repeatedly through multiple channels. Assume people need to hear it 7 times before it sinks in."""
        },
        
        "customer success strategy": {
            "keywords": ["customer success strategy", "cs strategy", "customer success playbook", "onboarding success", "expansion play", "qbr"],
            "insight": """Agent Vish Customer Success Playbook:
1. 90-DAY VALUE PLAN: Define 'first value' and 'full value' milestones by role. Publish a joint success plan in week 1 and review weekly.
2. HEALTH SCORING 2.0: Build a composite health score (adoption, outcomes, sentiment, risk signals). Automate alerts and playbooks for red/yellow accounts.
3. ONBOARDING BLUEPRINT: Time-box onboarding to 30-45 days with a RACI, training paths, and executive check-in at day 21.
4. QBR THAT SELL: Make QBRs narrative-driven: business goals -> outcomes -> gaps -> next bets. Close with a 2x2 roadmap and expansion hypothesis.
5. CS <> PRODUCT LOOP: Tag feedback to themes, quantify ARR-at-risk/ARR-opportunity, and feed a monthly Product-CS council.
6. RENEWALS AS A MOTION: Start 180 days out, confirm value proof, surface expansion bundle options, and pre-negotiate blockers."""
        },
        
        "f1 business best practices": {
            "keywords": ["f1 business", "formula 1", "pit stop ops", "race strategy", "f1 best practices", "f1 playbook"],
            "insight": """Agent Vish F1-Inspired Business Playbook:
1. PIT-STOP OPERATIONS: Design 'pit-stop' cadences for teams: 10-minute weekly maintenance, monthly tune-ups, quarterly overhauls.
2. TELEMETRY DASHBOARDS: Stream real-time KPIs like a race engineer. Alert thresholds, incident logs, and recovery playbooks.
3. STRATEGY UNDER UNCERTAINTY: Maintain A/B race plans with trigger conditions (market/weather). Pre-authorize pivots.
4. CREW EXCELLENCE: Role clarity drills, cross-training, and 'hot lap' simulations for critical launches.
5. TIRE MANAGEMENT ANALOGY: Balance burn rate vs. grip: stagger investments to sustain performance across the entire 'race season'."""
        },
        
        "video content analytics": {
            "keywords": ["video analytics", "watch time", "retention curve", "hook rate", "content performance", "video funnel"],
            "insight": """Agent Vish Video Analytics Framework:
1. FUNNEL METRICS: Track Hook Rate (0-3s), Hold Rate (3-30s), Completion Rate, CTR, and Return Viewers.
2. RETENTION CURVES: Annotate drops with content moments; test intros, pattern interrupts at 25/50/75%.
3. COHORTS & FORMAT: Compare performance by topic, length, format (shorts vs long-form), and thumbnail variants.
4. CONTENT ENGINE: Weekly idea->script->A/B thumbnail->publish->post-mortem loop with a 3-test minimum per video.
5. ROI MODEL: Attribute revenue to videos via UTMs and view-through conversions; prioritize topics with highest LTV per minute watched."""
        }
    }
    
    message_lower = message.lower()
    
    # Check for insight pattern matches
    for insight_topic, data in insight_patterns.items():
        for keyword in data["keywords"]:
            if keyword in message_lower:
                return data["insight"]
    
    return None


# Initialize bot and register all skills
if __name__ == "__main__":
    bot = AgenticAIBot()
    bot.add_skill(greet_skill)
    bot.add_skill(faq_skill)
   
