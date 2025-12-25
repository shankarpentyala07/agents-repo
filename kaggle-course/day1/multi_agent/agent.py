"""
You've just built your first multi-agent system! You used a single "coordinator" agent to manage the workflow, 
which is a powerful and flexible pattern.

‼️ However, relying on an LLM's instructions to control the order can sometimes be unpredictable. 
Next, we'll explore a different pattern that gives you guaranteed, step-by-step execution.
"""


from google.genai import types
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool,google_search
from google.adk.runners import InMemoryRunner

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a specalizied research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings",
)

print("research_agent created successfully")


summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""Read the provided research findings: {research_findings}
    Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)

root_agent = Agent(
    name="ResearchCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a research cooordinator.Your goal is to answer the user's query by orchestrating a workflow.
    1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
    2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
)
