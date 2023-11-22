from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.account_model import AccountModel
from core.deps import get_session

import requests

routerConvert = APIRouter()

@routerConvert.get('/{account_id}')
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