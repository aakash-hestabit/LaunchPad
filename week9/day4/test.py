import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from memory.memory_manager import MemoryManager
from dotenv import load_dotenv
import os
load_dotenv()

memory = MemoryManager()

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "openai",
        "context_length": 8192,
        "function_calling": True,
        "vision": True,
        "json_output": False,
        "structured_output":True
    },
)

Agent = AssistantAgent(
    name="SmartAgent",
    model_client=model_client,
    system_message="You have memory. Use provided context."
)

async def ask_agent():

    while True:

        user_input = input("USER (exit : to exit the chat):")

        if user_input.strip().lower()=="exit":
            print("BYE !!")
            break

        context = memory.retrieve_context(user_input)

        print(context)

        response = await Agent.run(
            task=TextMessage(
                content=f"STORED MEMORY RETRIEVALS: {context}\n Use the Retrieved Memory if relevant to User Query, And only respond to USER QUERY.\n\nUSER QUERY: {user_input}",
                source="user"
            )
        )

        answer = response.messages[-1].content
        memory.store_interaction(user_input, answer)
        print(f"AGENT: {answer}")

asyncio.run(ask_agent())