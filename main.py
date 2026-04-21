import uvicorn
from src.backend.api.server import app

if __name__ == "__main__":
    # Entry point for the entire application
    uvicorn.run("src.backend.api.server:app", host="0.0.0.0", port=8000, reload=True)
