# agent_vish.py
from skills.analytics_skill import analytics_skill

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
        "challenges as a team lead": "As a team lead, I've navigated several key challenges. One major aspect is balancing technical delivery with people management - ensuring the team stays productive while fostering their growth. I've handled situations where team members had conflicting priorities, and I addressed this by implementing clear communication channels and regular one-on-ones. Another challenge was managing cross-functional dependencies, which I resolved by establishing transparent roadmaps and proactive stakeholder updates.",
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
    return None


def insight_skill(message, memory):
    """
    Advanced skill function that delivers strategic, analytical, and actionable insights
    based on business growth, retention, leadership, career development, and performance analytics.
    Draws from real data and professional experience to provide consultative guidance.
    """
    insight_patterns = {
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


def report_skill(message, memory):
    """
    Analyze tabular data stored in memory['report_data'] (CSV string, list of dicts,
    or pandas-like DataFrame) when prompted with 'summarize report' or 'analyze spreadsheet'.
    Returns a comprehensive summary including:
    - total rows and columns
    - column names
    - total and average for each numeric column
    - top row (max) for each numeric metric
    - missing data info per column (count and percent)
    """
    triggers = ["summarize report", "analyze spreadsheet", "analyze sheet", "summarize spreadsheet", "summarize sheet"]
    q = message.lower()
    if not any(t in q for t in triggers):
        return None
    data = memory.get("report_data")
    if data is None:
        return "No report data found in memory['report_data']. Please load CSV/Excel content first."
    # Helper: try to coerce to a uniform table representation
    rows = []
    columns = []

    def is_number(x):
        try:
            if x is None or (isinstance(x, str) and x.strip() == ""):
                return False
            float(x)
            return True
        except Exception:
            return False

    # Case 1: pandas DataFrame-like (has to_dict and columns/shape attributes)
    try:
        if hasattr(data, "to_dict") and hasattr(data, "columns"):
            columns = list(data.columns)
            rows = [dict(zip(columns, row)) for row in data.values.tolist()]
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # list of dicts
            # collect union of keys as columns
            col_set = set()
            for r in data:
                col_set.update(r.keys())
            columns = list(col_set)
            # normalize rows (ensure all keys present)
            for r in data:
                rows.append({c: r.get(c) for c in columns})
        elif isinstance(data, str):
            # CSV text
            import csv, io
            reader = csv.DictReader(io.StringIO(data))
            columns = reader.fieldnames or []
            for r in reader:
                rows.append(dict(r))
        else:
            # Unknown format
            return "Unsupported report_data format. Provide CSV text, list of dicts, or a DataFrame."
    except Exception as e:
        return f"Failed to parse report_data: {e}"

    total_rows = len(rows)
    total_cols = len(columns)

    # Identify numeric columns by scanning values
    numeric_cols = []
    for c in columns:
        sample_vals = [r.get(c) for r in rows[:50]]  # sample to decide
        nums = [v for v in sample_vals if is_number(v)]
        if len(nums) >= max(1, int(0.2 * max(1, len(sample_vals)))):
            numeric_cols.append(c)

    # Compute totals, averages, top rows per numeric column
    totals = {}
    avgs = {}
    top_rows = {}
    for c in numeric_cols:
        vals = []
        for r in rows:
            v = r.get(c)
            if is_number(v):
                vals.append(float(v))
        if vals:
            totals[c] = sum(vals)
            avgs[c] = sum(vals) / len(vals)
            # find top row for max metric
            max_val = max(vals)
            # get first row with that max value
            for r in rows:
                v = r.get(c)
                if is_number(v) and float(v) == max_val:
                    top_rows[c] = {"value": max_val, "row": r}
                    break
        else:
            totals[c] = None
            avgs[c] = None
            top_rows[c] = None

    # Missing data per column
    missing_info = {}
    for c in columns:
        missing_count = 0
        for r in rows:
            v = r.get(c)
            if v is None or (isinstance(v, str) and v.strip() == ""):
                missing_count += 1
        pct = (missing_count / total_rows * 100.0) if total_rows else 0.0
        missing_info[c] = {"missing": missing_count, "percent": round(pct, 2)}

    # Build summary string
    from textwrap import shorten

    def fmt_row(row):
        # Keep row concise
        items = []
        for k in columns[:10]:  # limit to 10 columns for display
            v = row.get(k)
            s = str(v)
            items.append(f"{k}={shorten(s, width=60, placeholder='…')}")
        return ", ".join(items)

    lines = []
    lines.append("Report Summary:")
    lines.append(f"- Total rows: {total_rows}")
    lines.append(f"- Total columns: {total_cols}")
    lines.append(f"- Columns: {', '.join(columns)}")
    if numeric_cols:
        lines.append("- Numeric column stats:")
        for c in numeric_cols:
            t = totals.get(c)
            a = avgs.get(c)
            lines.append(f"  • {c}: total={t if t is not None else 'n/a'}, average={a if a is not None else 'n/a'}")
            tr = top_rows.get(c)
            if tr and tr.get("row"):
                lines.append(f"    top {c} value={tr['value']}, row: {fmt_row(tr['row'])}")
    else:
        lines.append("- No numeric columns detected.")

    lines.append("- Missing data per column:")
    for c in columns:
        info = missing_info[c]
        lines.append(f"  • {c}: missing={info['missing']} ({info['percent']}%)")

    return "\n".join(lines)


# Initialize bot and register all skills
if __name__ == "__main__":
    bot = AgenticAIBot()
    bot.add_skill(greet_skill)
    bot.add_skill(faq_skill)
    bot.add_skill(about_me_skill)
    bot.add_skill(insight_skill)
    bot.add_skill(report_skill)
    bot.add_skill(lambda msg, mem: analytics_skill(msg))
