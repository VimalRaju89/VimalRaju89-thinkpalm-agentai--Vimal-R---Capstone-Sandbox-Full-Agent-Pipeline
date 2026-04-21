import os
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite

class MemoryManager:
    """
    Handles persistent state for the agents using SQLite.
    """
    def __init__(self, db_path: str = "nexus_memory.db"):
        self.db_path = db_path

    def get_checkpointer(self):
        """
        Returns an asynchronous SqliteSaver for LangGraph.
        """
        return AsyncSqliteSaver.from_conn_string(self.db_path)

    @staticmethod
    async def init_db(db_path: str = "nexus_memory.db"):
        """
        Asynchronously initialize the database if needed.
        """
        async with aiosqlite.connect(db_path) as db:
            await db.execute("CREATE TABLE IF NOT EXISTS interactions (id INTEGER PRIMARY KEY, data TEXT)")
            await db.commit()
