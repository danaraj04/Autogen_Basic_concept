import asyncio
from dotenv import load_dotenv
load_dotenv()

import json
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1) Brain
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")


# 2) Agent (give it a name and a job)
assistant = AssistantAgent(
    name="storeteller",
    model_client=model_client,
    system_message="You are a helpful assistant with a good memory.",
)

# Tell the agent a fact in this conversation

# 3) Run it. In a notebook we use "await".
async def main():
    await Console(assistant.run_stream(
        task="Remember that my favourite number is 7."
    ))

# SAVE the state to a file (still inside main)
    state = await assistant.save_state()
    with open("agent_state.json", "w") as f:
        json.dump(state, f)
    print("Saved the conversation to agent_state.json")

# Run the main function
asyncio.run(main())
