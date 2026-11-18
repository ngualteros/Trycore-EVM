from fastapi import FastAPI

from app.routers import health

app = FastAPI(title="Trycore EVM API", docs_url="/api-docs", redoc_url=None)
app.include_router(health.router)
