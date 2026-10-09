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
# Custom tool 1: convert Fahrenheit to Celsius
def to_celsius(fahrenheit: float) -> float:
    """Convert a temperature from Fahrenheit to Celsius."""
    return round((fahrenheit - 32) * 5 / 9, 1)

# Custom tool 2: how many days until a given number of weeks
def weeks_to_days(weeks: int) -> int:
    """Return how many days are in the given number of weeks."""
    return weeks * 7

# Give the tool to the agent with tools=[...]

assistant = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[to_celsius, weeks_to_days],
    reflect_on_tool_use=True,
    system_message="You are a helpful assistant. Use your tools when needed.",
)

# 3) Run it. In a notebook we use "await".
async def main():
    result = await assistant.run(
        task="What is 98.6 Fahrenheit in Celsius? Also, how many days are in 3 weeks?"
    )

    # The agent's answer is the LAST message
    print(result.messages[-1].content)


# Run the main function
import asyncio

asyncio.run(main())