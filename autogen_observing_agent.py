import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1) Brain
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")


# 2) Agent (give it a name and a job)
assistant = AssistantAgent(
    name="storeteller",
    model_client=model_client,
    system_message="You are a friendly helper. Keep answers short.",
)

# 3) Run it. In a notebook we use "await".
async def main():
    await Console(assistant.run_stream(
        task="Give me one fun fact about the moon."
    ))

# Run the main function
import asyncio
asyncio.run(main())