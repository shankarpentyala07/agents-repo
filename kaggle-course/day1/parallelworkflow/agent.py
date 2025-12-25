"""
Sequential Agent Workflow is perfect for tasks that build on each other, but it's slow if the tasks are independent. 
Next, we'll look at how to run multiple agents at the same time to speed up your workflow.

sequential agent is great, but it's an assembly line. Each step must wait for the previous one to finish. What if you have several tasks that are not dependent on each other? For example, researching three different topics. Running them in sequence would be slow and inefficient, creating a bottleneck where each task waits unnecessarily.

The Solution: Concurrent Execution

When you have independent tasks, you can run them all at the same time using a ParallelAgent. This agent executes all of its sub-agents concurrently, dramatically speeding up the workflow. Once all parallel tasks are complete, you can then pass their combined results to a final 'aggregator' step.

Use Parallel when: Tasks are independent, speed matters, and you can execute concurrently.

"""


from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='<FILL_IN_MODEL>',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
