from google.adk.agents import LoopAgent
from google.adk.models import Gemini
from .agent import scriptWriterAgent, visualizerAgent, formatterAgent, retry_config
from .util import load_instruction_from_file

tube_shorts_agent = LoopAgent(
    name="youtube_shorts_loop_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="An agent that iteratively writes, visualizes, and formats a YouTube Short concept.",
    instruction="""You are an orchestrator. Your goal is to run a loop of agents to produce a final YouTube short concept.
1. First, call the ShortsScriptWriter to generate a script.
2. Next, call the ShortsVisualizer with the generated script.
3. Finally, call the ConceptFormatter to combine the script and visuals into a final output.
""",
    max_iterations=3,
    sub_agents=[
        scriptWriterAgent,
        visualizerAgent,
        formatterAgent
    ]
)

# --- Root Agent for the Runner ---
# The runner will now execute the workflow

root_agent = tube_shorts_agent
