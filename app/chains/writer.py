from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import llm

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior research analyst.

Write a deep and insightful report:
- Identify key trends
- Explain why they matter
- Include real-world implications
- Avoid generic explanations
- Be specific and analytical
"""),
    ("human", """
Write a structured report.

Topic: {topic}

Research:
{research}

Include:
- Introduction
- Key Points
- Analysis
- Conclusion
- Sources
""")
])

writer_chain = writer_prompt | llm | StrOutputParser()