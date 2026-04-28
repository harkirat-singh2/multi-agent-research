from langchain.tools import tool

@tool
def scrape_url(url: str) -> str:
    """Scrape a webpage and return cleaned readable content."""
    return f"Mock content extracted from {url}"