from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
from pydantic import BaseModel
from typing import List, Dict

class ValidationReport(BaseModel):
    requirements_met: List[str]
    requirements_missing: List[str]
    test_results: List[str]
    final_verdict: str

VALIDATOR_PROMPT = """
You are the Validator Agent. Your role is to verify that outputs meet all requirements and quality standards.

RESPONSIBILITIES:
- Extract explicit and implicit requirements from the task  
- Check functional correctness and expected behavior  
- Evaluate non-functional aspects: performance, security, reliability  
- Identify missing requirements, failures 

VALIDATION RULES:
- Test edge cases, and failure scenarios  
- Classify issues by severity and provide evidence  
- Security or data integrity failures are blockers  
- Deliver a clear final verdict: Approved, Conditional or Rejected
"""

validator_client = OllamaClient(ValidationReport).ollama_client

validator = AssistantAgent(
    name="validator",
    description="Ensures outputs strictly adhere to requirements and safety constraints",
    system_message=VALIDATOR_PROMPT,
    model_client=validator_client,
)