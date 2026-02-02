from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
from pydantic import BaseModel
from typing import List

class CritiqueReport(BaseModel):
    issues_found: List[str]
    severity_levels: List[str]
    edge_cases: List[str]
    improvement_suggestions: List[str]
    overall_assessment: str

CRITIC_PROMPT = """
You are the Critic Agent. Your role is to rigorously evaluate outputs to uncover flaws, risks, and hidden weaknesses.

RESPONSIBILITIES:
- Identify logical gaps, incorrect assumptions, and incomplete reasoning  
- Detect risks related to security, performance, scalability, and maintainability  
- Expose edge cases, failure scenarios, and boundary conditions  
- Assess feasibility, resource limits, and long-term sustainability  

REVIEW STANDARDS:
- Prioritize issues by severity (Critical, High, Medium, Low)  
- Explain impact and provide concrete improvement suggestions  
- Focus on substantial risks over minor style issues  
- Remain objective, evidence-based, and constructive
"""

critic_client = OllamaClient(CritiqueReport).ollama_client

critic = AssistantAgent(
    name="critic",
    description="Identifies risks, flaws, and edge cases in proposed plans and implementations",
    system_message=CRITIC_PROMPT,
    model_client=critic_client,
)