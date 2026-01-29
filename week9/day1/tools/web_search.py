import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def serp_search(query):
    API_KEY = os.environ["SERPAPI_KEY"]

    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://serpapi.com/search", params=params)

    return response.json()


def clean_serpapi_results(data):
    results = data.get("organic_results", [])
    
    cleaned = []
    for r in results[:5]:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        
        cleaned.append(f"""
SOURCE:
Title: {title}
Fact: {snippet}
URL: {link}
""")
    print()
    print(cleaned)
    print()
    print()
    return "\n".join(cleaned)


async def search_and_clean(query: str) -> str:
    """
    Searches the web and returns relevant results.
    INPUT:str
    OUTPUT:str
    """
    raw = await serp_search(query)
    return clean_serpapi_results(raw)
