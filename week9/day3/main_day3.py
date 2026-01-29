from pydantic import BaseModel, Field
from typing import List, Literal
import json
from autogen_agentchat.messages import TextMessage
from pydantic import ValidationError
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core import CancellationToken
import os
from agents.code_agent import CodeAgent
from agents.db_agent import DBAgent
from agents.file_agent import FileAgent
import asyncio
from tools.db_tools import extract_schema


AgentName = Literal["FileAgent", "DBAgent", "CodeAgent"]

class PlanStep(BaseModel):
    agent: AgentName
    instruction: str

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]

schema = extract_schema("sales.db")
PLANNER_SYSTEM_PROMPT = f"""
You are an Orchestrator Planner.

Your job:
1. Read the user request
2. Create a step-by-step execution plan
3. Decide which agent should do each step
4. Keep in mind the Data Paths as the database is shared among the Agents (Database path : "sales.db")

AVAILABLE AGENTS:
Each Agent is inpedendepnt and has specific roles
- FileAgent: inspect CSV, load CSV into SQLite, read/write .txt for the given path
- DBAgent: run SELECT/WITH SQL queries on SQLite (Only limited to reading Queries)
- CodeAgent: can GENERATE and  EXECUTES Python code as provided

STRICT RULES:
- Each Agent has independent roles as specified.
- The ORDER OF CALLING OF AGENTS IS CRITICAL and Output messages are shared sequentially Only, so generate the tasks in dependency order if the agents are dependent on each other.
- CSV data MUST be loaded into SQLite before  csv queries and analysis
- NEVER analyze CSV directly
- DBAgent must be used for all data analysis
- CodeAgent is OPTIONAL and only for computation
- Do NOT skip required steps
- DO NOT generate SQL, Give Simple Command to DBAgent if required.
- Database schema: {schema}
- Each Task generated for DBAgent SHOULD be INDEPENDENT and SHOULD be achieveable through the provided schema.
- Planner NEVER writes SQL queries.
- Planner gives high-level analytical instructions ad DB path only.
- DBAgent is responsible for converting instructions into SQL.
- Each DBAgent step must describe the independent analysis goal, not SQL syntax.
- Planner Should generate individual DBAgent tasks.
Output must strictly follow the provided schema.
Do not include explanations or extra text.
DO NOT add commentary.
ONLY return JSON.
"""


class LLMOrchestrator:
    def __init__(self, planner_llm, file_agent, db_agent, code_agent, summarizer_agent):
        self.planner_llm = planner_llm
        self.file_agent = file_agent
        self.db_agent = db_agent
        self.code_agent = code_agent
        self.summarizer_agent = summarizer_agent

        self.execution_log = []

    async def run(self, user_query: str) -> str:
        plan = await self._generate_plan(user_query)
        results = await self._execute_plan(plan)
        return await self.summarize_results(results)

    async def _generate_plan(self, user_query: str) -> ExecutionPlan:
        cancellation_token = CancellationToken()

        response = await self.planner_llm.on_messages(
            [
                TextMessage(content=PLANNER_SYSTEM_PROMPT, source="system"),
                TextMessage(content=user_query, source="user"),
            ],
            cancellation_token=cancellation_token,
        )

        raw_content = response.chat_message.content
        print("RAW PLANNER OUTPUT:\n", raw_content)

        try:
            plan_dict = json.loads(raw_content)
            plan = ExecutionPlan(**plan_dict)
            return plan
        except (json.JSONDecodeError, ValidationError) as e:
            raise RuntimeError(f"Invalid execution plan:\n{e}\n\nRAW:\n{raw_content}")


    async def _execute_plan(self, plan: ExecutionPlan) -> str:

        results = [] 

        for idx, step in enumerate(plan.steps, 1):

            agent = self._get_agent(step.agent)

            context = self._build_context(step, results)

            response = await agent.on_messages(
                [TextMessage(content=context, source="orchestrator")],
                cancellation_token=CancellationToken(),
            )

            output_text = response.chat_message.content
            agent_name = agent.name

            results.append({
                "agent": agent_name,
                "instruction": step.instruction,
                "output": output_text
            })

            self.execution_log.append({
                "step": idx,
                "agent": step.agent,
                "instruction": step.instruction,
                "output": output_text
            })

        return self._final_response()

    def _build_context(self,step,results):
        results = results[-3:]

        return f"""
You are performing a step in a multi-agent workflow.

CURRENT TASK:
{step.instruction}

RELEVANT PREVIOUS RESULTS:
{results}

Use previous outputs if needed.
RETURN ONLY YOUR RESULT.
"""


    def _get_agent(self, agent_name: str):
        if agent_name == "FileAgent":
            return self.file_agent
        if agent_name == "DBAgent":
            return self.db_agent
        if agent_name == "CodeAgent":
            return self.code_agent

        raise ValueError(f"Unknown agent: {agent_name}")

    def _final_response(self) -> str:
        lines = ["### Execution Complete\n"]

        for entry in self.execution_log:
            lines.append(f"#### Step {entry['step']} — {entry['agent']}")
            lines.append(f"Instruction: {entry['instruction']}")
            lines.append("Output:")
            lines.append(str(entry["output"]))
            lines.append("")

        return "\n".join(lines)
    
    async def summarize_results(self,results:str)->str:
        agent = self.summarizer_agent
        print(f"\n\n{results}\n\n")
        response = await agent.on_messages(
                [
                    TextMessage(
                        content=results,
                        source="orchestrator"
                    )
                ],
                cancellation_token=CancellationToken(),

            )

        return response.chat_message.content


# planner_model = OllamaChatCompletionClient(
#                     # model="mistral:7b-instruct-v0.3-q4_K_M",
#                     # model = 'mistral:7b-instruct-v0.3-q8_0'
#                     model = 'qwen3:8b',
#                     # model = 'mistral:7b-instruct',
#                     response_format = ExecutionPlan
#                 )

planner_model = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "llama",
        "context_length": 8192,
        "vision":True,
        "function_calling": False,
        "json_output": False,
        "structured_output": True
    },
    response_format = ExecutionPlan
)

PlannerAgent = AssistantAgent(
    name="PlannerAgent",
    model_client=planner_model,
    system_message="You generate execution plans only."
)



# summarizer_model = OllamaChatCompletionClient(
#                     # model="mistral:7b-instruct-v0.3-q4_K_M",
#                     # model = 'mistral:7b-instruct-v0.3-q8_0'
#                     model = 'qwen3:8b',
#                     # model = 'mistral:7b-instruct',
#                 )


summarizer_model = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("LLM_API_KEY"),
    model_info={
        "family": "llama",
        "context_length": 8192,
        "vision":True,
        "function_calling": False,
        "json_output": False,
        "structured_output": True
    },
)

summarizer_agent = AssistantAgent(
    name="Summarizer_Agent",
    description="Summarizes the resultsextracted from all the agents",
    model_client=summarizer_model,
    system_message="You are a Summarizer Agent.Your task is to summarize the results generated from different agents and give the user output in human readable format."
)


orchestrator = LLMOrchestrator(
    planner_llm=PlannerAgent,
    file_agent=FileAgent,
    db_agent=DBAgent,
    code_agent=CodeAgent,
    summarizer_agent= summarizer_agent
)



async def main():
    user_query = "Analyze sales.csv and generate top 5 insights"
    # user_query = "Write a python code to check 27 is prime or not and save the code and output in python.txt file"

    result = await orchestrator.run(user_query)

    print(result)

if __name__ == "__main__":
    asyncio.run(main())