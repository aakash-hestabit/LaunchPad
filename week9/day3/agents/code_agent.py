from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.code_executor import code_executor_tool
import os
from dotenv import load_dotenv

load_dotenv()
from autogen_ext.models.ollama import OllamaChatCompletionClient

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

CodeAgent = AssistantAgent(
    name="CodeAgent",
    model_client=model_client,
    system_message="""
You are a Python Code Execution Agent.

RULES:
- You CAN write new logic but ONLY if specefied EXPLICITLY. Otherwise You ONLY execute code exactly as provided.
- You execute the Python code provided by the user.
- You MUST always use the execute_python tool for code execution.
- You MUST return the real execution output.
- If execution fails, return the full error traceback.
""",
    tools=[code_executor_tool],
)