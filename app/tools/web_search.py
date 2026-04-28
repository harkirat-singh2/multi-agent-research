from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web and return relevant results including URLs and summaries."""
    return f"Mock search results for: {query} with URLs https://example.com"