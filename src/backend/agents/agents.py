from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from src.backend.tools.search import web_search

load_dotenv()

class BaseAgent:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0,
        )

class ResearcherAgent(BaseAgent):
    """
    Finds real-time information using web tools.
    """
    def __init__(self):
        super().__init__()
        self.llm_with_tools = self.llm.bind_tools([web_search])

    def run(self, state):
        messages = state["messages"]
        system_msg = SystemMessage(content=(
            "You are a World-Class Researcher. Use the web_search tool to find accurate, "
            "up-to-date information for the user's query. Be thorough and verify facts."
        ))

        try:
            response = self.llm_with_tools.invoke([system_msg] + messages)
            if getattr(response, "tool_calls", None):
                # If model still returns tool calls, force plain text output.
                response = self.llm.invoke([system_msg] + messages)
        except Exception as exc:
            err = str(exc)
            if "tool_use_failed" in err or "Failed to call a function" in err:
                # Fallback for model/provider combinations that reject tool calls.
                response = self.llm.invoke([system_msg] + messages)
            else:
                raise
        return {"messages": [response]}

class WriterAgent(BaseAgent):
    """
    Synthesizes research into a high-quality executive report.
    """
    def run(self, state):
        messages = state["messages"]
        
        system_msg = SystemMessage(content=(
            "You are a Professional Technical Writer. Your task is to take the research "
            "provided and synthesize it into a high-quality, glassmorphic-ready executive report. "
            "Use Markdown formatting, clear headings, and a professional tone."
        ))
        
        response = self.llm.invoke([system_msg] + messages)
        return {"final_report": response.content, "messages": [response]}
