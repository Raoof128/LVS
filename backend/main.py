from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import scan

app = FastAPI(
    title="LLM Vulnerability Scanner",
    description="OWASP Top 10 Compliance Scanner for Large Language Models",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(scan.router, prefix="/api/v1", tags=["Scan"])

# Serve Frontend
# In a real production setup, this would be served by Nginx or similar
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

@app.get("/")
async def root() -> dict:
    return {"message": "LLM Vulnerability Scanner API is running. Visit /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
