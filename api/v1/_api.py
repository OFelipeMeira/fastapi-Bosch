from fastapi import APIRouter
from api.v1.endpoints import account

api_router = APIRouter()
api_router.include_router(account.router, prefix='/accounts', tags=['Accounts'])
