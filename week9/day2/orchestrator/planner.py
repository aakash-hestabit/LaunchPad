from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import TextMessage
from typing import List
from loader import OllamaClient
from pydantic import BaseModel, Field

class Task(BaseModel):
    worker_name: str = Field(..., description="Name of the worker agent")
    task: str = Field(..., description="Concrete task to execute")
    instructions: str = Field(..., description="Execution instructions for the worker")


class PlannerResult(BaseModel):
    tasks: List[Task] = Field(..., description="List of tasks to be executed in parallel")



OllamaWapper= OllamaClient(PlannerResult)

ollama_client = OllamaWapper.ollama_client


class Planner:
    def __init__(self, worker_limit):
        self.planner = AssistantAgent(
            name="planner",
            model_client=ollama_client,
            system_message=(
                "You are a Planner Agent.\n"
                "Your job is to decompose the user request into parallel tasks.\n"
                "Each task must be executable independently.\n"
                f"The maximum number of workers assigned can be only {worker_limit} \n\n"
                "Return ONLY a JSON object that matches the PlannerResult schema.\n"
                "Do not include explanations or extra text."
            ),
        )

    async def run(self, user_task: str) -> PlannerResult:
        response = await self.planner.run(
            task = TextMessage(
                content=user_task,
                source="user"
            )
        )

        print(f"\n{response.messages[-1].content}\n\n")

    
        return response.messages[-1].content