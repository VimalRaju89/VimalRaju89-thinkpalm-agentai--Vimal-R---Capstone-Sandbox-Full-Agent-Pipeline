from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def web_search(query: str):
    """
    Search the web for real-time information using DuckDuckGo.
    Useful for finding latest news, facts, and research data.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

@tool
def save_research_note(content: str, research_data: list):
    """
    Saves a research note to the data accumulation list.
    """
    research_data.append(content)
    return f"Saved note: {content[:50]}..."
