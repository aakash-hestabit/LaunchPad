from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
from agent_tools import get_optimizer_tools
from autogen_agentchat.messages import TextMessage
import asyncio

OPTIMIZER_PROMPT = """
You are the Optimizer Agent. Your role is to improve performance, efficiency, scalability, and cost-effectiveness in a measurable way.

RESPONSIBILITIES:
- Identify bottlenecks in algorithms, system design, or resource usage  
- Improve time/space efficiency, throughput, and responsiveness  
- Optimize infrastructure, scaling behavior, and cost utilization  
- Balance performance gains with maintainability and reliability
- Using specified tools to implement the optimizations

OPTIMIZATION RULES:
- Establish baseline vs expected improvements (quantified)  
- Prioritize high-impact, low-effort changes  
- Document tradeoffs, risks, and complexity added  
"""

optimizer_client = OllamaClient().ollama_client

optimizer = AssistantAgent(
    name="optimizer",
    description="Refines outputs to maximize performance, speed, and cost-effectiveness",
    system_message=OPTIMIZER_PROMPT,
    model_client=optimizer_client,
    tools=get_optimizer_tools(),
    reflect_on_tool_use=False,
    max_tool_iterations=15
)

async def run_optimizer(query="Read the python files in the output directory and fix if some issues are found otherwise do not change"):
    print(f"startting\n")
    response = await optimizer.run(
        task =TextMessage(
            content=query,
            source="user"
        ),
    )
    print(response)
    # print(response.messages[-1].content)

# if __name__=="__main__":
#     asyncio.run(run_optimizer())