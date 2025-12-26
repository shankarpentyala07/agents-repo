"""
Loop Workflows - The Refinement Cycle
The Problem: One-Shot Quality

All the workflows we've seen so far run from start to finish. The SequentialAgent and ParallelAgent produce their final output and then stop. This 'one-shot' approach isn't good for tasks that require refinement and quality control. What if the first draft of our story is bad? We have no way to review it and ask for a rewrite.

The Solution: Iterative Refinement

When a task needs to be improved through cycles of feedback and revision, you can use a LoopAgent. A LoopAgent runs a set of sub-agents repeatedly until a specific condition is met or a maximum number of iterations is reached. This creates a refinement cycle, allowing the agent system to improve its own work over and over.

Use Loop when: Iterative improvement is needed, quality refinement matters, or you need repeated cycles.

Example: Iterative Story Refinement

"""
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool, google_search
from google.adk.tools.tool_context import ToolContext


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# This agent runs ONCE at the beginning to create the first draft.
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    description="Initially writes a short story based on the user's prompt.",
    output_key="current_story" ,# Stores the first draft in the state.
    tools=[google_search]  # Example tool usage, if needed.
)

# This agent's only job is to provide feedback or the approval signal. It has no tools.
critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}
    
    Evaluate the story's plot, characters and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.
    """,
    description="Critiques the current story and suggests improvements.",
    output_key="critique", # Stores the feedback in the state.
    tools=[google_search]
)

def exit_loop(tool_context: ToolContext) -> dict:
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no
    more changes are needed."""
    tool_context.actions.escalate = True
    return {"status": "approved", "message": "Story approved. Exiting refinement looop."}

research_agent = Agent(
    name="ResearchAgent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    instruction="""Use google_search if needed to gather facts.""",
    tools=[google_search],
    output_key="research_notes",
)

# This agent refines the story based on critique OR calls the exit_loop function.
refiner_agent = Agent(
    name="RefinerAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewtite the story draft to fully incorporate the feedback from the critique.""",
    description="Refines the story based on critique or exits if approved.",
    output_key="current_story", # It overwrites the story with the new, refined version.
    tools=[
        FunctionTool(exit_loop)
    ], # The tool is now correctly initialized with the function reference.
    )

# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[
        critic_agent,
        research_agent,
        refiner_agent
    ],
    max_iterations=2, # Prevent infinite loops by setting a max iteration count.
    description="Refines the story through critique and revision until approved."
)

# The root agent is a SequentialAgent that defines the overall workflow: Initial Write -> Refinement Loop.
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[
        initial_writer_agent,
        story_refinement_loop
    ],
)



