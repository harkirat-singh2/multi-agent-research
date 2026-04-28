from langchain.tools import tool
from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    response = client.search(query=query, max_results=3)

    results = []
    for r in response["results"]:
        results.append(f"{r['title']}\n{r['url']}\n{r['content']}")

    return "\n\n".join(results)