"""
Sequential Agent Workflow is perfect for tasks that build on each other, but it's slow if the tasks are independent. 
Next, we'll look at how to run multiple agents at the same time to speed up your workflow.

sequential agent is great, but it's an assembly line. Each step must wait for the previous one to finish. What if you have several tasks that are not dependent on each other? For example, researching three different topics. Running them in sequence would be slow and inefficient, creating a bottleneck where each task waits unnecessarily.

The Solution: Concurrent Execution

When you have independent tasks, you can run them all at the same time using a ParallelAgent. This agent executes all of its sub-agents concurrently, dramatically speeding up the workflow. Once all parallel tasks are complete, you can then pass their combined results to a final 'aggregator' step.

Use Parallel when: Tasks are independent, speed matters, and you can execute concurrently.

Let's build a system with four agents:

1. **Tech Researcher** - Researches AI/ML news and trends
2. **Health Researcher** - Researches recent medical news and trends
3. **Finance Researcher** - Researches finance and fintech news and trends
4. **Aggregator Agent** - Combines all research findings into a single summary

"""
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Tech Researcher: Focuses on AI and ML trends.
tech_researcher = Agent(
    name="TechResearcher",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
    the main companies involved, and the potential impact. keep the report very concise (100 words).""", 
    description="Researches latest AI/ML trends.",
    tools=[google_search],
    output_key="tech_research"
)

# Health Researcher: Focuses on medical breakthroughs.
health_researcher = Agent(
    name="HealthResearcher",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
    their practical applications, and estimated timelines. keep the report concise (100 words).""",
    description="Researches recent medical breakthroughs.",
    tools=[google_search],
    output_key="health_research"
)

# Finance Researcher: Focuses on fintech trends.
finance_researcher = Agent(
    name="FinanceResearcher",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),  
    instruction="""Research current fintech trends. Include 3 key trends,
    their market implications, and the future outlook. keep the report concise (100 words).""",
    description="Researches current fintech trends.",
    tools=[google_search],
    output_key="finance_research"
)

# The AggregatorAgent runs *after* the parallel step to synthesize the results.
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these three research findings into a single executive summary:

    ** Technology Trends:**
    {tech_research}

    ** Health Breakthroughs:**
    {health_research}

    **Finance Innovations:**
    {finance_research}

    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    description="Combines research findings into a single summary.",
    output_key="executive_summary"
)

# The ParallelAgent runs all its sub-agents simultaneously.
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[
        tech_researcher,
        health_researcher,
        finance_researcher
    ],
    description="Executes multiple research agents in parallel."
)

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[
        parallel_research_team,
        aggregator_agent
    ],
)

