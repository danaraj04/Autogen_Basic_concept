from dotenv import load_dotenv
load_dotenv()
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def main():
    # 1) Brain
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    # 2) Make a memory and add some facts to remember
    memory = ListMemory()
    await memory.add(MemoryContent(content="The user's name is Danaraj", mime_type=MemoryMimeType.TEXT))
    await memory.add(MemoryContent(content="The user loves cricket.", mime_type=MemoryMimeType.TEXT))

    # 3) Give the memory (and tools) to the agent
    searcher = AssistantAgent(
        name="searcher",
        model_client=model_client,
        memory=[memory],
        # tools=[...],
    )

    result = await searcher.run(task="What sport do I like?")
    print(result.messages[-1].content)

    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())