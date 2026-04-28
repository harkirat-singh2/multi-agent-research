from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import llm

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a strict research evaluator.

Critique based on:
- Depth of analysis
- Accuracy
- Missing insights
- Practical usefulness

Be critical and specific.
"""),
    ("human", """
Review the report:

{report}

Give:
Score: X/10
Strengths:
Weaknesses:
Suggestions:
""")
])

critic_chain = critic_prompt | llm | StrOutputParser()