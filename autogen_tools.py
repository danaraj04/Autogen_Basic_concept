import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1) Brain
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# A tool is just a normal Python function with a short docstring.
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Give the tool to the agent with tools=[...]

math_agent = AssistantAgent(
    name="math_agent",
    model_client=model_client,
    tools=[add],
    reflect_on_tool_use=True,
    system_message="You are a math helper. Use your tools to calculate.",
)

# 3) Run it. In a notebook we use "await".
async def main():
    await Console(math_agent.run_stream(
        task="What is 124 plus 376?"
    ))

# Run the main function
import asyncio
asyncio.run(main())