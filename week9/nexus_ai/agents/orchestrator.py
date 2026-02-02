import asyncio
import json
import os
import shutil
from collections import defaultdict, deque
from autogen_agentchat.messages import TextMessage

from config import MAX_RETRIES_PER_AGENT, MAX_PLAN_RETRIES, LOG_FILE_PATH, OUTPUT_DIR
from tools import create_log_entry
from memory.memory_manager import MemoryManager
from agents.planner import planner, ExecutionPlan
from agents.researcher import researcher
from agents.coder import coder
from agents.analyst import analyst
from agents.critic import critic
from agents.optimizer import optimizer
from agents.validator import validator
from agents.reporter import reporter

AGENT_REGISTRY = {
    "Researcher": researcher,
    "Coder": coder,
    "Analyst": analyst,
    "Critic": critic,
    "Optimizer": optimizer,
    "Validator": validator,
    "Reporter": reporter,
}

memory_manager = MemoryManager()

def compute_levels(execution_plan):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for step in execution_plan.steps:
        in_degree[step.agent] = len(step.depends_on)
        for dep in step.depends_on:
            graph[dep].append(step.agent)

    queue = deque([n for n in in_degree if in_degree[n] == 0])
    levels = []

    while queue:
        level = list(queue)
        levels.append(level)
        next_queue = deque()

        for node in level:
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_queue.append(neighbor)

        queue = next_queue

    return levels


async def run_agent_with_retry(agent_name, instruction, global_context, user_query):
    agent = AGENT_REGISTRY[agent_name]
    last_error = None

    for attempt in range(MAX_RETRIES_PER_AGENT):

        retry_info = f"\nPREVIOUS FAILURE:\n{last_error}\nFix the issue.\n" if last_error else ""
        global_context = compress_context(global_context)
        prompt = f"""
SYSTEM GOAL (USER REQUEST):
{user_query}

YOUR TASK:
{instruction}

CONTEXT FROM PREVIOUS AGENTS:
{global_context}

{retry_info}
"""
        try:
            print(f"\n running {agent_name} Agent")
            result = await agent.run(task=TextMessage(content=prompt, source="orchestrator"))
            output = result.messages[-1].content

            memory_manager.store_interaction(agent_name, output)

            create_log_entry(LOG_FILE_PATH, agent_name.lower(), "success", {"output": output})
            return {"agent": agent_name, "success": True, "output": output}

        except Exception as e:
            last_error = str(e)
            create_log_entry(LOG_FILE_PATH, agent_name.lower(), "retry", {"attempt": attempt + 1, "error": last_error})

    return {"agent": agent_name, "success": False, "error": last_error}


async def run_level(level_agents, step_map, context, user_query):
    tasks = [
        run_agent_with_retry(agent, step_map[agent], context, user_query)
        for agent in level_agents
    ]
    return await asyncio.gather(*tasks)


async def execute_plan(execution_plan, user_query):
    levels = compute_levels(execution_plan)
    step_map = {step.agent: step.instruction for step in execution_plan.steps}
    global_context = {}

    for level_agents in levels:
        level_results = await run_level(level_agents, step_map, global_context, user_query)

        for res in level_results:

            if not res["success"]:
                raise Exception(f"EXEC_FAIL::{res['agent']}::{res['error']}")

            global_context[res["agent"]] = res["output"]

            if res["agent"] == "Validator":
                if "FAIL" in res["output"].upper() or "REJECTED" in res["output"].upper():
                    raise Exception(f"VALIDATION_FAIL::{res['output']}")

    return global_context

def compress_context(context, limit=1200):
    return {k: v[:limit] for k, v in context.items()}


async def run_autonomous_loop(initial_plan, user_query):
    current_plan = initial_plan
    validator_feedback = None

    for attempt in range(MAX_PLAN_RETRIES):
        print(f"\n ATTEMPT {attempt+1}/{MAX_PLAN_RETRIES} ")

        try:
            return await execute_plan(current_plan, user_query)

        except Exception as e:
            err = str(e)

            if err.startswith("VALIDATION_FAIL::"):
                validator_feedback = err.replace("VALIDATION_FAIL::", "")
                memory_manager.store_interaction("validator_feedback", validator_feedback)

                clear_output_dir()

                replan_prompt = f"""
SYSTEM GOAL:
{user_query}

VALIDATOR FEEDBACK:
{validator_feedback}

Generate a NEW improved execution plan fixing these issues.
"""

                result = await planner.run(task=TextMessage(content=replan_prompt, source="orchestrator"))
                plan_data = json.loads(result.messages[-1].content)
                create_log_entry(LOG_FILE_PATH, "planner", "updated_plan_generated", {"steps": plan_data})
                current_plan = ExecutionPlan(**plan_data)
                continue

            raise

    raise Exception("System failed after maximum plan retries.")


def clear_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        return
    for f in os.listdir(OUTPUT_DIR):
        p = os.path.join(OUTPUT_DIR, f)
        try:
            if os.path.isfile(p):
                os.unlink(p)
            else:
                shutil.rmtree(p)
        except:
            pass
