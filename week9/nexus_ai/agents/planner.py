from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from loader import OllamaClient
from pydantic import BaseModel, Field
from typing import Literal, List, Optional
import asyncio

AgentName = Literal["Researcher", "Coder", "Analyst", "Critic", "Optimizer", "Validator", "Reporter"]

class PlanStep(BaseModel):
    agent: AgentName
    instruction: str
    depends_on: List[AgentName] = Field(default_factory=list)


class ExecutionPlan(BaseModel):
    steps: List[PlanStep]

# class PlanStep(BaseModel):
#     agent:AgentName
#     instruction: str

# class ExecutionPlan(BaseModel):
#     steps: List[PlanStep]


PLANNER_PROMPT = """
You are an expert Planner Agent for a multi-agent system.

Your job is to:
1. Decompose complex user queries into concrete execution steps
2. Assign each step to the most appropriate agent
3. Return a structured plan following the ExecutionPlan schema

- Do NOT execute tasks
- Do NOT analyze data

Available Agents and Their Roles:
- Researcher: Research, data gathering, competitive analysis
- Analyst: Data analysis, statistical analysis, business intelligence
- Coder: Code generation, architecture design, technical implementation
- Critic: Review, critique, quality assessment, feedback
- Optimizer: Performance optimization, efficiency improvements
- Validator: Validation of result and is the Solution alligned to user needs (should be near the end)
- Reporter: Final report generation, documentation (should be last)

AVAILABLE TOOLS FOR AGENTS:
Coder: read/write source files, create JSON configs, inspect project structure.
Analyst: read CSV/JSON/FILE data, compute column statistics, inspect data files and project structure.
Optimizer: read and rewrite code/configs to improve performance and efficiency, inspect project structure.
Reporter: read artifacts and logs, write reports and documentation.

IMPORTANT:
- Think about which steps can run independently (in parallel)
- Generate ATMOST one instance of each Agent
- Use dependencies to control execution order
- Implement parallelization where logical
- Return ONLY valid JSON matching ExecutionPlan schema
- Do not include explanations or markdown formatting

CRITICAL: Identify dependencies between steps to enable parallel execution
Dependency Rules:
- Steps with NO dependencies (dependencies: []) can run FIRST and IN PARALLEL
- Steps that depend on other steps must list those agent names in dependencies
- Multiple independent steps can run in parallel (good for performance)
- Validator should depend on most agents
- Reporter should depend on Validator (runs last)
- We Need to Generate a Directed Acyclic Graph for parallel an sequential execution with different levels of agents

PLANNING METHODOLOGY:
1. Understand the user request and final deliverable
2. Identify required knowledge, artifacts, and validations
3. Ensure logical dependencies are respected
4. Include quality gates (Critic, Validator) at appropriate points
5. Assign only one task to one Agent
6. Use one Agent ATMOST once
7. If any agent is NOT required to perform the query DO NOT include it
"""

planner_client = OllamaClient(ExecutionPlan).ollama_client

planner = AssistantAgent(
    name="planner",
    description="Generates sequential execution plans by assigning tasks to specialized agents",
    system_message=PLANNER_PROMPT,
    model_client=planner_client,
    

)

async def run_planner(query="plan an ai healthcare startup"):

    result = await planner.run(
        task = TextMessage(
            content=query,
            source="user"
        )
    )
    print(result.messages[-1].content)


# asyncio.run(run_planner())