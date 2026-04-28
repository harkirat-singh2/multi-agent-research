from langchain.agents import create_agent
from app.core.config import llm
from app.tools.web_search import web_search


def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a research assistant.

Use web_search to find reliable information.
Return:
- Title
- URL
- Summary
"""
    )