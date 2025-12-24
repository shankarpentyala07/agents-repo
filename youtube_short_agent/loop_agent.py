from google.adk.agents import LoopAgent
from google.adk.models import Gemini
from .agent import scriptWriterAgent, visualizerAgent, formatterAgent, retry_config
from .util import load_instruction_from_file

tube_shorts_agent = LoopAgent(
    name="youtube_shorts_loop_agent",
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
