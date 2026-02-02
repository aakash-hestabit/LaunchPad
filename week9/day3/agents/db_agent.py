from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from tools.db_tools import schema_query_tool, extract_schema_tool
import os
from dotenv import load_dotenv

from dotenv import load_dotenv

load_dotenv()


# model_client = OllamaChatCompletionClient(
#                     # model="mistral:7b-instruct-v0.3-q4_K_M",
#                     # model = 'mistral:7b-instruct-v0.3-q8_0'
#                     model = 'qwen3:8b',
#                     # model = 'mistral:7b-instruct',
#                 )

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "llama",
        "context_length": 8192,
        "function_calling": True,
        "vision": True,
        "json_output": False,
        "structured_output":True
    },
    parallel_tool_calls=False
)


DBAgent = AssistantAgent(
    name="DBAgent",
    model_client=model_client,
    system_message=f"""
You are a Database Agent.

STRICT RULES:
- You NEVER assume table or column names.
- ALWAYS extract the DATABASE SCHEMA using the tool.
- You MUST always use the schema_aware_query tool.
- You ONLY generate SELECT or WITH SQL queries.
- You MUST limit the number of rows where-ever possible.
- You base your answer ONLY on tool results.
- If the query fails, analyze the error and retry with a corrected query.
""",
    tools=[extract_schema_tool, schema_query_tool],
    max_tool_iterations=10
)
