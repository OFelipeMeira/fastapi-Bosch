from fastapi import APIRouter
from api.v1.endpoints import accounts

api_router = APIRouter()
api_router.include_router(accounts.router, prefix='/accounts', tags=['Accounts'])
