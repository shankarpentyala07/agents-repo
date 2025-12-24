from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.models import Gemini
from google.genai import types
from .util import load_instruction_from_file


retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)


# sub Agent 1 - Script Writer

scriptWriterAgent = LlmAgent(
    name="ShortsScriptWriter",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A script writer that generates short-form content for social media platforms like TikTok, Instagram Reels, and YouTube Shorts.",
    instruction=load_instruction_from_file('scriptwriter_instruction.txt'),
    tools=[google_search],
    output_key = "generated_script" # Save results to state
)

# sub Agent 2 - Visualizer
visualizerAgent = LlmAgent(
    name="ShortsVisualizer",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A visualizer that creates engaging visual content based on the generated script for social media platforms like TikTok, Instagram Reels, and YouTube Shorts.",
    instruction=load_instruction_from_file('visualizer_instruction.txt'),
    output_key = "visual_concepts" # Save results to state
)

# sub Agent 3 - Formatter
formatterAgent = LlmAgent(
    name="ConceptFormatter",   
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Formats the final short concept",    
    instruction="""Combine the script from state['generated_script'] with the visual concepts from state['visual_concepts'] into the final Markdown format requested previously (Hook, Script & Visuals table, Visual Notes, CTA).""",
    output_key = "final_short_concept" # Save results to state
)

# LLM Agent
youtube_shorts_agent = LlmAgent(
    name="youtube_shorts_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="You are an agent that can write scripts, visuals and format youtube short videos. You have subagents that can do this.",
    instruction=load_instruction_from_file('shorts_agent_instruction.txt'), # Load instruction from file
    tools=[
        AgentTool(scriptWriterAgent),
        AgentTool(visualizerAgent),
        AgentTool(formatterAgent)
    ],
)


# --- Root Agent for the Runner ---
# The runner will now execute the workflow

root_agent = youtube_shorts_agent
