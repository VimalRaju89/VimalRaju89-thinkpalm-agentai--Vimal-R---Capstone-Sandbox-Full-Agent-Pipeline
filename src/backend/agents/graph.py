from langgraph.graph import StateGraph, END
from src.backend.core.state import AgentState
from src.backend.agents.agents import ResearcherAgent, WriterAgent
import os

def create_graph(checkpointer=None):
    # Initialize agents
    researcher = ResearcherAgent()
    writer = WriterAgent()
    
    # Define the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", researcher.run)
    workflow.add_node("writer", writer.run)
    
    # Set entry point
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    return workflow.compile(checkpointer=checkpointer)
