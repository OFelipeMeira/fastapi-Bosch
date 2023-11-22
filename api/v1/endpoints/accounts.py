from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.account_model import AccountModel
from schemas.account_schema import AccountSchema, CreateAccountSchema
from core.deps import get_session

routerCrud = APIRouter()

@routerCrud.get('/')
async def get_all_accounts(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query  = select(AccountModel)
        result = await session.execute(query)
        accounts: List[AccountModel] = result.scalars().all()
        return {"data":accounts}

@routerCrud.get('/{account_id}', response_model=AccountSchema, status_code=status.HTTP_200_OK )
async def get_single_account(account_id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query  = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account  = result.scalar_one_or_none()
        return account

@routerCrud.post('/', status_code=status.HTTP_201_CREATED, response_model=CreateAccountSchema)
async def create_account(account: CreateAccountSchema, db: AsyncSession = Depends(get_session)):
    new_account = AccountModel(id = 0,
                               firstName = account.firstName,
                               lastName = account.lastName,
                               cpf = account.cpf,
                               brl = 0)
    db.add(new_account)
    await db.commit()
    return new_account

@routerCrud.put('/{account_id}', response_model= CreateAccountSchema, status_code=status.HTTP_202_ACCEPTED )
async def update_account(account_id:int, account: CreateAccountSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AccountModel).filter(AccountModel.id == account_id)
        result = await session.execute(query)
        account_update = result.scalar_one_or_none()
        if account_update:
            account_update.firstName = account.firstName
            account_update.lastName  = account.lastName
            account_update.cpf       = account.cpf
            await session.commit()
            return account_update
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not founded..."))

@routerCrud.delete('/{account_id}', status_code=status.HTTP_204_NO_CONTENT)
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

            