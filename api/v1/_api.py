from fastapi import APIRouter
from api.v1.endpoints import cursos

api_router = APIRouter()
api_router.include_router(cursos.router, prefix='/cursos', tags=['cursos'])
