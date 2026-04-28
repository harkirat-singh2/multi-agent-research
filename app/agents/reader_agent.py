from langchain.agents import create_agent
from app.core.config import llm
from app.tools.scraper import scrape_url

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
Extract clean and useful content from webpages.
Remove noise and summarize key insights.
"""
    )