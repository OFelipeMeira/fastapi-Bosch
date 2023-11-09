from fastapi import APIRouter
from api.v1.endpoints import person

api_router = APIRouter()
api_router.include_router(person.router, prefix='/persons', tags=['Persons'])
