from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from loader import OllamaClient

ollama_client = OllamaClient().ollama_client

class WorkerAgent:
    def __init__(self, name: str, task: str, instructions: str):
        self.agent = AssistantAgent(
            name=name,
            model_client=ollama_client,
            system_message=(
                "You are a Worker Agent.\n"
                "You execute ONLY the task assigned to you.\n"
                f"Your task is:\n{task}\n"
                f"Follow the instructions:\n{instructions}\n"
                "Be concise and factual.\n"
                "Do not reflect or validate. \n"
            ),
        )

    # async def run(self, task: str, instructions: str, execution_tree:list):

    #     print(f"Running {self.agent.name} Agent")
    #     execution_tree[-1].append(f"Running {self.agent.name} Agent")

    #     response = await self.agent.run(
    #         task = TextMessage(
    #             content=f"task: {task}. Instructions: {instructions}",
    #             source="user"
    #         )
    #     )

    #     print(f"Completed {self.agent.name} Agent")
        
    #     return response.messages[-1].content