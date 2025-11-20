from __future__ import annotations

from fastapi import APIRouter, FastAPI

from app.routers import projects, scenes


api = APIRouter()
api.include_router(projects.router, prefix='/projects', tags=['projects'])
api.include_router(scenes.router, prefix='/scenes', tags=['scenes'])

app = FastAPI(
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc',
)
app.include_router(api, prefix='/api')
