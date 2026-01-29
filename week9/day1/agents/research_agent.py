from autogen_agentchat.agents import AssistantAgent
from tools.tool_registry import web_search_tool
from loader import OllamaClient
ollama_client = OllamaClient().ollama_client

print("starting research agent")

researcher = AssistantAgent(
    name="research_agent",
    system_message=(
        "You are a Research Agent.\n"
        "Use ReAct format:\n"
        "Thought -> Action -> Observation -> Final\n\n"
        "Collect factual info from web using the tools if required.\n"
        "Do NOT summarize and answer in full detail.\n"
    ),
    tools=[web_search_tool],
    model_client=ollama_client,
)