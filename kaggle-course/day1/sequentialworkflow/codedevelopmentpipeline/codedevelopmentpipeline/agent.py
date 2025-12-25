"""
The Problem: Unpredictable Order

The previous multi-agent system worked, but it relied on a detailed instruction prompt to force the LLM to run steps in order. This can be unreliable. A complex LLM might decide to skip a step, run them in the wrong order, or get "stuck," making the process unpredictable.

The Solution: A Fixed Pipeline

When you need tasks to happen in a guaranteed, specific order, you can use a SequentialAgent. This agent acts like an assembly line, running each sub-agent in the exact order you list them. The output of one agent automatically becomes the input for the next, creating a predictable and reliable workflow.

Use Sequential when: Order matters, you need a linear pipeline, or each step builds on the previous one.

This is perfect for tasks that build on each other, but it's slow if the tasks are independent

"""


from google.genai import types
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


code_writer_agent = Agent(
    name="CodeWriterAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a Python Code Generator.
    Based *only* on the user's request, write Python code that fulfills the requirement.
    Output *only* the complete Python code block, enclosed in triple backticks (```python...```).
    Do not add any other text before or after the code block.
    """,
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"
)


code_reviewer_agent = Agent(
    name="CodeReviewerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are an expert Python Code Reviewer.
    Your task is to provide constructive feedback on the provided Python code.

    **Code to Review:**
    ```python
    {generated_code}
    ```
    **Review Criteria:**
    1. **Correctness**: Does the code work as intended? Are there logic errors?
    2. **Readability**: Is the code clear and easy to understand? Follow PEP 8 guidelines?
    3. **Efficiency**: Is the code reasonably efficient? Any obvious performance bottlenecks?
    4. **Edge Cases**: Does the code handle potential edge cases or invalid inputs gracefully?
    5. **Best Practices**: Does the code follow common Python best practices?

    **Output:**
    Provide your feedback as a concise, bulleted list.Foucs on the most important points for improvement.
    If the code is excellent and requires no changes, simply state: "No major issues found."
    Output *on;y* the review comments or the "No major issues" statement.
    """,
    description="Reviews code and provides feedback.",
    output_key="review_comments"
)

code_refactorer_agent = Agent(
    name="CodeRefactorerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),  
    instruction="""You are a Python Code Refactoring AI.
    Your goal is to improve the provided Python code based on the provided review comments.

    **Original Code:**
    ```python
    {generated_code}
    ```
    **Review Comments:**
    {review_comments}

    **Task:**
    Carefully apply the suggestions from the review comments to refactor the original code.
    If the review comments state "No major issues found," return the original code unchanged.
    Ensure the final code is complete, functional, and includes necessary imports and docstrings.

    **Output:**
    Output *only* the final, refactored Python code block, enclosed in triple backticks (```python...```).
    Do not add any other text before or after the code block.
    """,
    description="Refactors code based on review comments.",
    output_key="refactored_code"
)

# --- 2. Create the SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order

code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[
        code_writer_agent,
        code_reviewer_agent,
        code_refactorer_agent
    ],
    description="Executes a sequence of code writing, reviewing, and refactoring."
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
    )

root_agent = code_pipeline_agent