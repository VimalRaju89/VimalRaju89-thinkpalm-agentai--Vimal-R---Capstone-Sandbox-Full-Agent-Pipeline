from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import time
from dotenv import load_dotenv
from src.backend.agents.graph import create_graph
from src.backend.core.memory import MemoryManager
from langchain_core.messages import HumanMessage
from contextlib import asynccontextmanager
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle the lifecycle of the graph and its checkpointer.
    """
    memory = MemoryManager()
    logger.info("Starting API lifespan and initializing graph")
    # AsyncSqliteSaver.from_conn_string returns an async context manager
    async with AsyncSqliteSaver.from_conn_string(memory.db_path) as saver:
        app.state.graph = create_graph(checkpointer=saver)
        logger.info("Graph initialized successfully")
        yield
    logger.info("API lifespan shutdown complete")

app = FastAPI(
    title="Nexus Intelligence API",
    lifespan=lifespan
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str
    thread_id: str

@app.get("/")
def read_root():
    logger.info("Health check requested at root endpoint")
    return {"status": "Nexus Intelligence Suite is online"}

@app.post("/research")
async def run_research(research_req: ResearchRequest, request: Request):
    """
    Trigger the multi-agent pipeline for a specific query.
    """
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": research_req.thread_id}}
    start = time.perf_counter()
    logger.info(
        "Research request started | thread_id=%s | query_preview=%s",
        research_req.thread_id,
        research_req.query[:120],
    )
    input_state = {
        "messages": [HumanMessage(content=research_req.query)],
        "research_data": [],
        "plan": "",
        "next_step": "",
        "final_report": ""
    }
    
    try:
        # Run the graph
        result = await graph.ainvoke(input_state, config=config)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Research request completed | thread_id=%s | duration_ms=%.2f",
            research_req.thread_id,
            duration_ms,
        )
        return {
            "thread_id": research_req.thread_id,
            "final_report": result.get("final_report", "No report generated."),
            "history": [msg.content for msg in result.get("messages", [])]
        }
    except Exception as e:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(
            "Research request failed | thread_id=%s | duration_ms=%.2f",
            research_req.thread_id,
            duration_ms,
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{thread_id}")
async def get_history(thread_id: str, request: Request):
    """
    Retrieve history for a specific thread from memory.
    """
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": thread_id}}
    logger.info("History requested | thread_id=%s", thread_id)
    state = await graph.aget_state(config)
    if not state.values:
        logger.info("History empty | thread_id=%s", thread_id)
        return {"messages": []}
    logger.info("History found | thread_id=%s", thread_id)
    return {
        "messages": [msg.content for msg in state.values.get("messages", [])],
        "final_report": state.values.get("final_report", "")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
