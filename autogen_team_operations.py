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

writer = AssistantAgent(name="writer", model_client=model_client,
                        system_message="Write one short slogan. Improve it if asked.")

reviewer = AssistantAgent(name="reviewer", model_client=model_client, 
                          system_message="If the slogan is catchy, reply APPROVE. Else suggest one change.")

# Stop when APPROVE appears OR after 6 messages (whichever comes first)
stop = TextMentionTermination("APPROVE") | MaxMessageTermination(6)
team = RoundRobinGroupChat([writer, reviewer], termination_condition=stop)

# 3) Run it. In a notebook we use "await".
# Watch the team work LIVE with Console
async def main():
    await Console(team.run_stream(task="Create a slogan for a coffee shop."))

    # Clear the team's memory of the coffee slogan
    await team.reset()
    # Now run a brand-new, unrelated task
    result = await team.run(task="Create a slogan for a book store.")
    print(result.messages[-1].content)
# Run the main function
import asyncio

asyncio.run(main())