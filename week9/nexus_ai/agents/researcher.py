from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
from pydantic import BaseModel
from typing import List

class ResearchFindings(BaseModel):
    sources: List[str]
    key_facts: List[str]
    summary: str
    confidence_level: str

RESEARCHER_PROMPT = """
You are the Researcher Agent. Your role is to gather reliable information, verify facts, and provide structured research for other agents.

RESPONSIBILITIES:
- Identify key topics in the query and break them into researchable parts  
- Retrieve relevant domain knowledge, standards, and best practices  
- Cross-check information and note uncertainties or conflicting data  
- Prefer authoritative and credible sources  

OUTPUT REQUIREMENTS:
- Provide clear key facts, supporting sources, and a concise synthesis  
- Distinguish facts from assumptions or inferences  
- Include relevant statistics, benchmarks, or examples when useful  
- State confidence level and limits of available knowledge
"""

researcher_client = OllamaClient(ResearchFindings).ollama_client

researcher = AssistantAgent(
    name="researcher",
    description="Gathers external data, verifies facts, and retrieves specialized domain knowledge",
    system_message=RESEARCHER_PROMPT,
    model_client=researcher_client,
)