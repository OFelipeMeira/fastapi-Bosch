from fastapi import APIRouter, status, HTTPException, Response
from database import connector, models
from schemas.account import AccountSchema


router = APIRouter()

@router.get('/')
async def get_accounts():
    await connector.connect()
    data = await models.Account.all()
    await connector.disconnect()
    
    return {'data': data}

@router.post('/')
async def create_account(account: AccountSchema, service: PostService = Depends(post_factory)):
    await connector.connect()
    data = await models.Account.create()
    await connector.disconnect()

    return {'data': data}