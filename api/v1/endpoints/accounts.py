from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.account_model import AccountModel
from schemas.account_schema import AccountSchema
from core.deps import get_session

import requests

router = APIRouter()

@router.get('/')
async def get_accounts(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query  = select(AccountModel)
        result = await session.execute(query)
        accounts: List[AccountModel] = result.scalars().all()
        return {"data":accounts}

@router.get('/{account_id}', response_model=AccountSchema, status_code=status.HTTP_200_OK)
async def get_account(account_id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query  = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account  = result.scalar_one_or_none()
        return account

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AccountSchema)
async def post_account(account: AccountSchema, db: AsyncSession = Depends(get_session)):
    new_account = AccountModel(id = 0,
                             firstName = account.firstName,
                             lastName = account.lastName,
                             cpf = account.cpf,
                             brl = account.brl,
                            )
    db.add(new_account)
    await db.commit()
    return new_account

@router.put('/{account_id}', response_model= AccountSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_account(account_id:int, account: AccountSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account_update = result.scalar_one_or_none()
        if account_update:
            account_update.firstName = account.firstName
            account_update.lastName  = account.lastName
            account_update.cpf       = account.cpf
            account_update.brl       = account.brl
            await session.commit()
            return account_update
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not founded..."))

@router.delete('/{account_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id:int , db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account_del = result.scalar_one_or_none()
        if account_del:
            await session.delete(account_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not founded..."))

@router.get('/{account_id}/convert', tags=["Convert"])
async def get_account_conversion(account_id:int, db: AsyncSession = Depends(get_session), quota:str=""):
    async with db as session:
        query  = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account  = result.scalar_one_or_none()

        url = "http://api.exchangeratesapi.io/v1/latest?access_key=ee694924a67ecd528d6cc2288d7cf245&format=2"    
        response = requests.get(url=url).json()

        balance_BRL = account.brl
        value_BRL = response["rates"]["BRL"]

        if quota == "":
            balances = {}
            for key in response['rates'].keys():
                balances[key] = float(response["rates"][key]) * float(balance_BRL)  / float(value_BRL)
            return {"data": balances}
        else:
            try:
                conversion =  float(response["rates"][quota.upper()]) * float(balance_BRL)  / float(value_BRL)
                return {"data": conversion}
            except:
                raise(HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quota not founded"))