from autogen_agentchat.agents import AssistantAgent
from loader import OllamaClient
from autogen_agentchat.messages import TextMessage
from agent_tools import get_analyst_tools
import asyncio

ANALYST_PROMPT = """
You are the Analyst Agent. Your role is to interpret data and turn it into evidence-based insights and decisions.

RESPONSIBILITIES:
- Understand the business objective and context before analyzing  
- Evaluate data quality, gaps, and potential biases  
- Identify key metrics, trends, patterns, outliers, and relationships  
- Quantify findings and support them with evidence  
- Reading the local files and analysing if applicable using the available tools only

ANALYTICAL OUTPUT:
- Translate results into clear insights tied to business impact  
- Provide actionable, prioritized recommendations
- Highlight risks, uncertainties, and alternative scenarios  
- Distinguish facts from assumptions and state confidence level
- Try that the genrated analysis are not too small or too large
"""

analyst_client = OllamaClient().ollama_client

analyst = AssistantAgent(
    name="analyst",
    description="Interprets datasets to extract trends, correlations, and strategic insights",
    system_message=ANALYST_PROMPT,
    model_client=analyst_client,
    tools=get_analyst_tools(),
    reflect_on_tool_use=False,
    max_tool_iterations=15
)

async def run_analyst(query="a file sales.csv is loacted in the root folder ,Analyze this file and create business strategy"):
    print(f"startting\n")
    response = await analyst.run(
        task =TextMessage(
            content=query,
            source="user"
        ),
    )
    print(response)
    print(response.messages[-1].content)

# if __name__=="__main__":
#     asyncio.run(run_analyst())