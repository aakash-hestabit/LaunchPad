from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
ollama_client = OllamaClient().ollama_client

answer_agent = AssistantAgent(
    name="answer_agent",
    system_message=(
        "You are an Answer Agent.\n"
        "Answer ONLY using the summary and be relevent to the query.\n"
        "If info is missing, say 'Not enough data.'\n"
    ),
    model_client=ollama_client,
)