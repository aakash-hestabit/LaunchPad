# import asyncio
# import json
# import os
# import shutil
# from autogen_agentchat.messages import TextMessage
# from tools import create_log_entry
# from agents.analyst import analyst
# from agents.coder import coder
# from agents.critic import critic 
# from agents.optimizer import optimizer
# from agents.planner import planner, ExecutionPlan
# from agents.reporter import reporter
# from agents.researcher import researcher
# from agents.validator import validator
# import config
# from config import *

# AGENT_REGISTRY = {
#     "Researcher": researcher,
#     "Coder": coder,
#     "Analyst": analyst,
#     "Critic": critic,
#     "Optimizer": optimizer,
#     "Validator": validator,
#     "Reporter": reporter,
# }
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(LOG_DIR, exist_ok=True)

# async def generate_execution_plan(query)-> ExecutionPlan:
    
#     try:
#         result = await planner.run(
#             task=TextMessage(content=query, source="user")
#         )
        
#         plan_content = result.messages[-1].content
        
#         create_log_entry(
#             log_file=LOG_FILE_PATH,
#             agent_name="planner",
#             action="generate_plan",
#             details={"query": query, "plan": plan_content}
#         )
        
#         if isinstance(plan_content, str):
#             plan_data = json.loads(plan_content)
#         else:
#             plan_data = plan_content
        
#         execution_plan = ExecutionPlan(**plan_data)
                
#         for idx, step in enumerate(execution_plan.steps, 1):
#             print(f"  Step {idx}: {step.agent}")
#             print(f"    Instruction: {step.instruction}\n")
        
#         memory_manager.store_interaction(plan_content)
        
#         return execution_plan
        
#     except Exception as e:
#         print(f"error while planning phase: {str(e)}")
#         raise


# async def execute_step(step, step_number, context):
    
#     agent = AGENT_REGISTRY.get(step.agent)
    
#     if not agent:
#         error_msg = f"Agent '{step.agent}' not found in registry"
#         print(f"ERROR: {error_msg}")
#         return {"error": error_msg, "agent": step.agent}
    
#     try:
#         context_info = f"\n\nContext from previous steps:\n{json.dumps(context, indent=2)}" if context else ""
#         full_instruction = f"{step.instruction}{context_info}"
        
#         result = await agent.run(
#             task=TextMessage(content=full_instruction, source="orchestrator")
#         )
        
#         output = result.messages[-1].content

#         if step.agent == "Validator" and "FAIL" in output.upper():
#             raise Exception(f"Validation failed: {output}")
        
#         create_log_entry(
#             log_file=LOG_FILE_PATH,
#             agent_name=step.agent.lower(),
#             action="execute_step",
#             details={
#                 "step_number": step_number,
#                 "instruction": step.instruction,
#                 "output": str(output)[:500] 
#             }
#         )
        
#         print(f"{step.agent} completed successfully")
        
#         memory_manager.store_interaction(output)
        
#         return {
#             "agent": step.agent,
#             "instruction": step.instruction,
#             "output": output,
#             "success": True
#         }
        
#     except Exception as e:
#         error_msg = f"Error executing {step.agent}: {str(e)}"
#         print(f"ERROR: {error_msg}")
        
#         create_log_entry(
#             log_file=LOG_FILE_PATH,
#             agent_name=step.agent.lower(),
#             action="execute_step_failed",
#             details={
#                 "step_number": step_number,
#                 "instruction": step.instruction,
#                 "error": error_msg
#             }
#         )
        
#         return {
#             "agent": step.agent,
#             "instruction": step.instruction,
#             "error": error_msg,
#             "success": False
#         }


# async def execute_plan(execution_plan: ExecutionPlan, query:str):
   
#     results = []
#     context = {}
    
#     for idx, step in enumerate(execution_plan.steps, 1):
#         step_result = await execute_step(step, idx, context)
#         results.append(step_result)
        
#         if step_result.get("success"):
#             context[f"{step.agent}_output"] = step_result.get("output")
        
#         if not step_result.get("success"):

#             error_str = str(step_result.get("error", ""))
#             if "429" in error_str or "rate_limit_exceeded" in error_str:
#                 print(f"\n ERROR: API Rate Limit Reached (429). Terminating all subsequent steps.")
#                 return results
            
#             if step.agent=="Validator" and config.MAX_RETRIES>0:
#                 replan_prompt = f"""
# The previous plan failed validation.

# ORIGINAL USER QUERY:
# {query}

# PREVIOUS PLAN:
# {execution_plan.model_dump_json(indent=2)}

# VALIDATOR FEEDBACK:
# {step_result}

# Generate a corrected execution plan that fixes these issues.
# """
#                 print("Retrying as the Validator failed")
#                 config.MAX_RETRIES-=1
#                 clear_output_dir()
#                 new_plan =await generate_execution_plan(replan_prompt)
#                 return await execute_plan(new_plan,replan_prompt)

#             else:
#                 print(f"\nWARNING: Step {idx} failed. Continuing with remaining steps...")
    
#     return results



# async def generate_final_report(query, results, execution_plan:ExecutionPlan) :
    
#     report_content = f"""# NEXUS AI Execution Report

# ## Query
# {query}

# """
#     for idx, result in enumerate(results):
#         report_content += f"### Step {idx+1}: {execution_plan.steps[idx].agent}\n\n"
#         report_content += f"**Instruction:** {execution_plan.steps[idx].instruction}\n\n"
#         report_content += f"**Output:** {result}\n"
#         report_content += "---\n"
    
    
#     report_path = os.path.join(OUTPUT_DIR, "EXCECUTION_REPORT.md")
#     os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
#     with open(report_path, 'w', encoding='utf-8') as f:
#         f.write(report_content)

#     return report_path


# def clear_output_dir():
#     if not os.path.exists(OUTPUT_DIR):
#         return

#     for filename in os.listdir(OUTPUT_DIR):
#         file_path = os.path.join(OUTPUT_DIR, filename)

#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)     
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)  
#         except Exception as e:
#             print(f"Failed to delete {file_path}. Reason: {e}")

#     print("OUTPUT_DIR cleared for fresh execution.")

# async def run_nexus(query):

#     try:
#         execution_plan = await generate_execution_plan(query)
        
#         results = await execute_plan(execution_plan, query)
        
#         report_path = await generate_final_report(query, results, execution_plan)
        
#         return {
#             "success": True,
#             "query": query,
#             "report_path": report_path,
#             "results": results
#         }
        
#     except Exception as e:
#         print(f"\nCRITICAL ERROR: {str(e)}")
#         return {
#             "success": False,
#             "query": query,
#             "error": str(e)
#         }

# async def main():
#     try:
#         query = input("USER: ")
        
#         result = await run_nexus(query)
            
#     except KeyboardInterrupt:
#         print("\n\n[NEXUS] Execution interrupted by user")
#     except Exception as e:
#         print(f"\n[NEXUS] Error: {str(e)}")


# if __name__ == "__main__":
#     asyncio.run(main())

#######################################################################
########################## DAG BASED GRAPHFLOW EXECUTION ##########################
#######################################################################

# import asyncio
# import json
# import os
# import shutil
# from datetime import datetime
# from typing import Dict, List

# from autogen_agentchat.messages import TextMessage
# from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
# from autogen_agentchat.conditions import MaxMessageTermination

# from tools import create_log_entry
# from agents.analyst import analyst
# from agents.coder import coder
# from agents.critic import critic
# from agents.optimizer import optimizer
# from agents.planner import planner, ExecutionPlan
# from agents.reporter import reporter
# from agents.researcher import researcher
# from agents.validator import validator
# from memory.memory_manager import MemoryManager
# import config
# from config import *

# AGENT_REGISTRY = {
#     "Researcher": researcher,
#     "Coder": coder,
#     "Analyst": analyst,
#     "Critic": critic,
#     "Optimizer": optimizer,
#     "Validator": validator,
#     "Reporter": reporter,
# }

# memory_manager = MemoryManager()

# def initialize_workspace():
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     os.makedirs(LOG_DIR, exist_ok=True)


# async def generate_execution_plan(query) -> ExecutionPlan:
#     memory_context = memory_manager.retrieve_context(query)

#     enhanced_query = f"{query}\n\nMEMORY CONTEXT:\n{memory_context}"

#     result = await planner.run(task=TextMessage(content=enhanced_query, source="user"))
#     plan_data = json.loads(result.messages[-1].content)

#     execution_plan = ExecutionPlan(**plan_data)

#     create_log_entry(
#         LOG_FILE_PATH,
#         "planner",
#         "generate_plan",
#         {"query": query, "steps": len(execution_plan.steps)},
#     )

#     print(f"\n {execution_plan}\n\n\n")

#     return execution_plan


# def build_parallel_graph(execution_plan: ExecutionPlan):
#     builder = DiGraphBuilder()
#     agent_instances = {}

#     for step in execution_plan.steps:
#         agent = AGENT_REGISTRY[step.agent]
#         agent_instances[step.agent] = agent
#         builder.add_node(agent)

#     for step in execution_plan.steps:
#         for dep in step.depends_on:
#             builder.add_edge(
#                 agent_instances[dep],
#                 agent_instances[step.agent]
#             )

#     if "Validator" in agent_instances:
#         for step in execution_plan.steps:
#             if step.agent not in ["Validator", "Reporter"]:
#                 builder.add_edge(
#                     agent_instances[step.agent],
#                     agent_instances["Validator"],
#                 )

#     if "Reporter" in agent_instances and "Validator" in agent_instances:
#         builder.add_edge(agent_instances["Validator"], agent_instances["Reporter"])

#     for step in execution_plan.steps:
#         if not step.depends_on:
#             builder.set_entry_point(agent_instances[step.agent])

#     return builder, builder.build(), agent_instances


# def build_agent_task_map(execution_plan: ExecutionPlan):
#     return {step.agent: step.instruction for step in execution_plan.steps}


# async def execute_plan_parallel(execution_plan: ExecutionPlan, query: str):
#     builder, graph, agent_instances = build_parallel_graph(execution_plan)
#     agent_task_map = build_agent_task_map(execution_plan)

#     team = GraphFlow(
#         participants=builder.get_participants(),
#         graph=graph,
#         termination_condition=MaxMessageTermination(40),
#     )

#     content = f"ORIGINAL QUERY: {query}\n\n"
#     for step in execution_plan.steps:
#         content += f"TASK FOR {step.agent}:\n{step.instruction}\n\n"
    
#     result = await team.run(task=content)

#     agent_outputs = {}
#     for msg in result.messages:
#         if msg.source in agent_instances:
#             agent_outputs[msg.source] = msg.content

#             memory_manager.store_interaction(
#                 f"{query} -> {msg.source}", str(msg.content)[:1000]
#             )

#             create_log_entry(
#                 LOG_FILE_PATH,
#                 msg.source.lower(),
#                 "parallel_execute",
#                 {"output": str(msg.content)[:500]},
#             )

#     validator_output = agent_outputs.get("Validator", "")
#     print(validator_output)
#     if "FAIL" in validator_output.upper():
#         raise Exception(f"Validation failed: {validator_output}")

#     return [{"agent": k, "output": v, "success": True} for k, v in agent_outputs.items()]


# async def run_with_retries(plan, query, retries=2):
#     """
#     Execute plan with retry logic.
#     IMPORTANT: Only regenerate plan on structural errors, not validation failures.
#     """
#     original_query = query
    
#     for attempt in range(retries):
#         try:
#             print(f"ATTEMPT {attempt + 1}/{retries}")
            
#             return await execute_plan_parallel(plan, original_query)
            
#         except Exception as e:
#             error_msg = str(e)
#             print(f"\nAttempt {attempt + 1} failed: {error_msg}\n")
            
#             memory_manager.store_interaction(
#                 f"{original_query}_retry_{attempt}", 
#                 f"Error: {error_msg}"
#             )
            
#             if attempt < retries - 1:
#                 clear_output_dir()
                
#                 if "validation failed" not in error_msg.lower():
#                     print("Regenerating execution plan due to error")
#                     plan = await generate_execution_plan(
#                         f"{original_query}\n\nPREVIOUS ERROR: {error_msg}\n\n"
#                         "Please create a more robust plan to avoid this error."
#                     )
    
#     raise Exception(f"Max retries ({retries}) reached. Last error: {error_msg}")


# def clear_output_dir():
#     if not os.path.exists(OUTPUT_DIR):
#         return
#     for f in os.listdir(OUTPUT_DIR):
#         p = os.path.join(OUTPUT_DIR, f)
#         try:
#             if os.path.isfile(p):
#                 os.unlink(p)
#             else:
#                 shutil.rmtree(p)
#         except Exception as e:
#             print(f"Warning: Could not delete {p}: {e}")


# async def run_nexus(query):

#     print(f"Query: {query}\n")
    
#     initialize_workspace()
    
#     execution_plan = await generate_execution_plan(query)
    
#     results = await run_with_retries(execution_plan, query)
    
#     return {"success": True, "results": results}


# async def main():
#     query = input("Enter your task: ")
#     try:
#         result = await run_nexus(query)
#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import json
import os
import shutil
from autogen_agentchat.messages import TextMessage
from agents.planner import planner, ExecutionPlan
from agents.orchestrator import run_autonomous_loop, memory_manager
from config import OUTPUT_DIR, LOG_DIR, LOG_FILE_PATH
from tools import create_log_entry



def initialize_workspace():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


async def generate_execution_plan(query) -> ExecutionPlan:
    memory_context = memory_manager.retrieve_context(query)
    enhanced_query = f"{query}\n\nMEMORY CONTEXT:\n{memory_context}"

    result = await planner.run(task=TextMessage(content=enhanced_query, source="user"))
    plan_data = json.loads(result.messages[-1].content)

    execution_plan = ExecutionPlan(**plan_data)

    create_log_entry(LOG_FILE_PATH, "planner", "plan_generated", {"steps": plan_data})

    return execution_plan


async def run_nexus(query):
    print(f"\nUSER QUERY: {query}\n")

    initialize_workspace()

    execution_plan = await generate_execution_plan(query)

    results = await run_autonomous_loop(execution_plan, query)

    return {"success": True, "results": results}

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
        except Exception as e:
            print(f"Warning: Could not delete {p}: {e}")


async def main():
    query = input("Enter your task: ")

    try:
        result = await run_nexus(query)
        print("\nEXECUTION COMPLETE\n")

    except Exception as e:
        print(f"\nSYSTEM ERROR: {e}")
        create_log_entry(LOG_FILE_PATH, "system", "fatal_error", {"error": str(e)})


if __name__ == "__main__":
    asyncio.run(main())
