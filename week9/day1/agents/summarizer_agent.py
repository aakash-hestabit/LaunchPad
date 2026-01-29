from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
ollama_client = OllamaClient().ollama_client

summarizer = AssistantAgent(
    name="summarizer_agent",
    system_message=(
        "You are a Summarizer Agent.\n"
        "Your job is to extract key facts.\n"
        "No opinions.\n"
        "Return bullet points.\n"
    ),
    model_client=ollama_client,
)