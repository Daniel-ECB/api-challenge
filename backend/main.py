from fastapi import Depends, FastAPI
from app.api.v1.router import api_router


app = FastAPI()

# Mount the v1 router with the global /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}