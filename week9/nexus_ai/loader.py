import os
from dotenv import load_dotenv
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
load_dotenv()
print(os.environ['LLM_API_KEY'])

class OllamaClient:
    def __init__(self, response_structure = None):
        if response_structure:
                # self.ollama_client = OllamaChatCompletionClient(
                #     # model="mistral:7b-instruct-v0.3-q4_K_M",
                #     # model = 'mistral:7b-instruct-v0.3-q8_0'
                #     model = 'qwen3:8b',
                #     # model = 'mistral:7b-instruct',
                #     response_format = response_structure
                # )

                self.ollama_client = OpenAIChatCompletionClient(
                    model="openai/gpt-oss-120b",
                    # model='openai/gpt-oss-20b',
                    # model="llama-3.3-70b-versatile",
                    # model='meta-llama/llama-4-maverick-17b-128e-instruct',
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ['LLM_API_KEY'],
                    model_info={
                        "family": "llama",
                        "context_length": 8192,
                        "function_calling": True,
                        "vision": True,
                        "json_output": False,
                        "structured_output":True
                    },
                    response_format = response_structure
                )
        else:
                # self.ollama_client = OllamaChatCompletionClient(
                #     # model="mistral:7b-instruct-v0.3-q4_K_M",
                #     # model = 'mistral:7b-instruct-v0.3-q8_0'
                #     model = 'qwen3:8b',
                #     # model = 'mistral:7b-instruct',
                # )
        
                self.ollama_client = OpenAIChatCompletionClient(
                    model="openai/gpt-oss-120b",
                    # model='openai/gpt-oss-20b',
                    # model="llama-3.3-70b-versatile",
                    # model="meta-llama/llama-4-maverick-17b-128e-instruct",
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ['LLM_API_KEY'],
                    model_info={
                        "family": "llama",
                        "context_length": 8192,
                        "function_calling": True,
                        "vision": True,
                        "json_output": False,
                        "structured_output":True
                    },
                )
