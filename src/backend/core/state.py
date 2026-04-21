from typing import Annotated, List, TypedDict, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    State for the Nexus Intelligence Suite.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    research_data: List[str]
    plan: str
    next_step: str
    final_report: str
