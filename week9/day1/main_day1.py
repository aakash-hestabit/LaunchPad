import asyncio 
from agents.answer_agent import answer_agent
from agents.research_agent import researcher
from agents.summarizer_agent import summarizer
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def main():

    query = input("What would you like to research today? ")

    research = await researcher.run(task=query)
    research_text = research.messages[-1].content

    summary = await summarizer.run(
        task=f"[RESEARCH DATA]\n{research_text}"
    )
    summary_text = summary.messages[-1].content

    final = await answer_agent.run(
        task=f"[QUERY]\n{query}\n\n[SUMMARY]\n{summary_text}"
    )
    print(research.messages)
    print()
    print()
    print("\nFINAL ANSWER:\n", final.messages[-1].content)
    

if __name__ == "__main__":
    asyncio.run(main())