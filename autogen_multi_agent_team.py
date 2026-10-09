import asyncio
from dotenv import load_dotenv
load_dotenv()

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1) Brain
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Agent 1: the writer
writer = AssistantAgent(name="writer", model_client=model_client,
                        system_message="You write a short birthday message. Improve it if the reviewer asks.")
# Agent 2: the reviewer
reviewer = AssistantAgent(name="reviewer", model_client=model_client, 
                          system_message="Review the message. If it is good, reply with the single word APPROVE. Otherwise suggest one change.")

# Stop when APPROVE appears OR after 6 messages (whichever comes first)
stop = TextMentionTermination("APPROVE") | MaxMessageTermination(6)
team = RoundRobinGroupChat([writer, reviewer], termination_condition=stop)

# 3) Run it. In a notebook we use "await".
async def main():
    result = await team.run(task="Write a warm birthday message for my friend Arulraj.")
    # Print the whole conversation
    for m in result.messages:
        print(f"[{m.source}] {m.content}\n")


# Run the main function
import asyncio
asyncio.run(main())