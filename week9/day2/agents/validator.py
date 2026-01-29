from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import TextMessage
from typing import List
from pydantic import BaseModel, Field
from loader import OllamaClient


class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether the answer is valid")
    issues: List[str] = Field(default_factory=list, description="Validation issues")




OllamaWapper= OllamaClient(ValidationResult)

ollama_client = OllamaWapper.ollama_client


class ValidatorAgent:
    def __init__(self):
        self.agent = AssistantAgent(
            name="validator",
            model_client=ollama_client,
            system_message=(
                "You are a Validator Agent.\n"
                "Your job is to verify the correctness and completeness of the given answer.\n"
                "Check for factual errors, missing steps, contradictions, or vague claims.\n"
                "Do NOT rewrite or improve the answer.\n"
                "Return ONLY a JSON object matching the ValidationResult schema."
            ),
            
        )

    async def run(self, answer: str) -> ValidationResult:

        # execution_tree.append(["Running Validator Agent"])

        response = await self.agent.run(
            task = TextMessage(
                content=answer,
                source="user"
            )
        )
        
        print(f"\n{response.messages[-1].content}\n\n")
        
        return response.messages[-1].content
