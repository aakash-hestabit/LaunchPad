import asyncio 
import json
from loader import OllamaClient
from orchestrator.planner import Planner
from agents.worker_agents import WorkerAgent
from agents.validator import ValidatorAgent
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import DiGraphBuilder
from autogen_agentchat.teams import GraphFlow


ollama_client = OllamaClient().ollama_client

WORKER_LIMIT = 3

reflector = AssistantAgent(
    name="reflector",
    model_client=ollama_client,
    system_message=(
        "You are a Reflection Agent.\n"
        "You receive outputs from multiple worker agents.\n"
        "Your job is to synthesize them into a single, coherent, high-quality response.\n"
        "Improve clarity, remove redundancy, and structure the answer logically.\n"
        "Do NOT add new facts.\n"
        "Do NOT validate correctness.\n"
        "Return only the improved answer."
    )
)

execution_tree = []


def get_execution_levels(graph):
    parents = graph.get_parents()
    levels = []
    assigned = set()

    while len(assigned) < len(graph.nodes):
        level = []

        for node in graph.nodes:
            if node in assigned:
                continue

            node_parents = parents.get(node, [])
            if all(p in assigned for p in node_parents):
                level.append(node)

        if not level:
            raise ValueError("Cycle detected in graph")

        levels.append(level)
        assigned.update(level)

    return levels


async def main():

    query = input("what would you like to perform today? ")

    plan = await Planner(WORKER_LIMIT).run(query)

    try:
        plan = json.loads(plan)
    except json.JSONDecodeError:
        clean_plan = plan.strip().replace("```json", "").replace("```", "")
        plan = json.loads(clean_plan)

    builder = DiGraphBuilder()

    builder.add_node(reflector)
    validator = ValidatorAgent().agent
    builder.add_node(validator)

    workers = []

    for task in plan["tasks"]:
        worker = WorkerAgent(task['worker_name'], task['task'], task['instructions'])
        workers.append(worker.agent)
        builder.add_node(worker.agent)
        builder.add_edge(worker.agent,reflector)
    
    builder.add_edge(reflector, validator)

    graph = builder.build()

    levels = get_execution_levels(graph)
    
    team = GraphFlow(
        participants=[*workers, reflector, validator],
        graph=graph,
    )

    result = await team.run(task="START")

    validator_output = None
    reflector_output = None

    for msg in result.messages:
        if msg.source == "validator":
            validator_output = msg.content
        elif msg.source == "reflector":
            reflector_output = msg.content

    validation = json.loads(
        validator_output.strip().replace("```json", "").replace("```", "")
    )

    if validation["is_valid"]:
        print("\n FINAL ANSWER:\n")
        print(reflector_output)
    else:
        print("\n VALIDATION FAILED\n")
        print("Generated Response: \n")
        print(f"{reflector_output}\n")
        print("Validation Failed due to the following issues.")
        for issue in validation["issues"]:
            print("-", issue)

    

    print("\nEXECUTION TREE (LEVELS)\n")
    print(f"START: QUERY - ['{query}']")

    print("   |")
    print(f"   |-- Level {-1}: ['Planner']")

    for i, level in enumerate(levels):
        print("   |")
        print(f"   |-- Level {i}: {level}")

    print("   |")
    print("['FINAL OUTPUT']")


if __name__=="__main__":
    asyncio.run(main())