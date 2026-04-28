import re

def extract_urls(text):
    return list(set(re.findall(r'https?://\S+', text)))


def safe_invoke(agent, payload):
    try:
        result = agent.invoke(payload)
        return result["messages"][-1].content
    except Exception as e:
        return f"ERROR: {str(e)}"