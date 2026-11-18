from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

from app.routers import activities, evm, health, projects
from app.services.common import ResourceNotFound

app = FastAPI(title="Trycore EVM API", docs_url="/api-docs", redoc_url=None)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(activities.router)
app.include_router(evm.router)


@app.exception_handler(ResourceNotFound)
async def resource_not_found(request: Request, exc: ResourceNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(IntegrityError)
@app.exception_handler(DataError)
async def invalid_database_data(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=422, content={"detail": "Data violates storage constraints"}
    )


@app.exception_handler(SQLAlchemyError)
async def database_unavailable(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=503, content={"detail": "Database temporarily unavailable"}
    )
