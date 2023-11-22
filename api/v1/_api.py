from fastapi import APIRouter
from api.v1.endpoints import accounts, transfer, convert

api_router = APIRouter()
api_router.include_router(accounts.routerCrud,     prefix='/accounts', tags=['Accounts'])
api_router.include_router(transfer.routerTransfer, prefix='/transfer', tags=['Transfer'])
api_router.include_router(convert.routerConvert,   prefix='/convert',  tags=['Conversion'])
