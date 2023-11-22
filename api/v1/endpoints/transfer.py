from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.account_model import AccountModel
from schemas.account_schema import ValueSchema
from decimal import Decimal
from core.deps import get_session

routerTransfer = APIRouter()

@routerTransfer.post('/deposit/{acccount_id}')
async def deposit(account_id:int, valueSchema: ValueSchema ,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(account_id == AccountModel.id)
        result = await session.execute(query)
        account = result.scalar_one_or_none()

        if valueSchema.value < 0:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value must be greater than 0"))

        if not account:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not founded"))
        
        account.brl += Decimal(valueSchema.value)
        await session.commit()
        return {"result": f"added R${valueSchema.value} to {account.firstName} {account.lastName}"}
        
            
@routerTransfer.post('/withdraw/{acccount_id}')
async def withdraw(account_id:int, valueSchema: ValueSchema ,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(account_id == AccountModel.id)
        result = await session.execute(query)
        
        account = result.scalar_one_or_none()

        # verify if the value is avaliable
        if valueSchema.value < 0:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value must be greater than 0"))

        # verify if this account exists
        if not account:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not founded"))
        
        # verify if the account has enough money
        if account.brl < valueSchema.value:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{account.firstName} {account.lastName} don't have enough money"))
        

        account.brl -= Decimal(valueSchema.value)
        await session.commit()
        return {"result": f"Drawee {valueSchema.value} to {account.firstName} {account.lastName}"}
    
@routerTransfer.post('/{sender_account_id}/{receiver_account_id}')
async def transfer(sender_account_id:int,receiver_account_id:int, valueSchema: ValueSchema ,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(sender_account_id == AccountModel.id)
        result = await session.execute(query)
        sender_account = result.scalar_one_or_none()
        
        query = select(AccountModel).filter(receiver_account_id == AccountModel.id)
        result = await session.execute(query)
        receiver_account = result.scalar_one_or_none()

        # verify if the value is avaliable
        if valueSchema.value < 0:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value must be greater than 0"))

        # verify if this account exists
        if not sender_account or not receiver_account:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not founded"))
        
        # verify if the account has enough money
        if sender_account.brl < valueSchema.value:
            raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{sender_account.firstName} {sender_account.lastName} don't have enough money"))
        

        sender_account.brl   -= Decimal(valueSchema.value)
        receiver_account.brl += Decimal(valueSchema.value)
        await session.commit()
        return {"result": f"Transaction Done"}