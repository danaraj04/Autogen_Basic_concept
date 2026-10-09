import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1) Brain
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")


# 2) Agent (give it a name and a job)
assistant = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="You are a friendly helper. Keep answers short.",
)

# 3) Run it. In a notebook we use "await".
async def main():
    result = await assistant.run(
        task="Give me one fun fact about the moon."
    )

    # The agent's answer is the LAST message
    print(result.messages[-1].content)


# Run the main function
import asyncio

asyncio.run(main())