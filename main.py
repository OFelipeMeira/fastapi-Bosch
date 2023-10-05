from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import database
import requests

app = FastAPI()

@app.get("/", tags=['Accounts'])
async def home():
    """
    Method to test Api connection - 'Hello World'
    """
    return {"message": "Hello Word"}


@app.post("/v1/accounts", tags=['Accounts'])
async def create_account(account: database.Account):
#         /register
    """
    Method to create new account onto the database
    :param: account - type: Account Model
    """
    if account:
        database.new_account(account=account)
        return {'message': f"Account {account.name} created"}
    else:
        return {'message': f"Account not created"}


@app.get("/v1/accounts", tags=['Accounts'])
async def get_accounts():
#         /v1/accountss
    """
    Method to return all accounts from the database
    """
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response}


@app.get("/v1/accounts/{account_CPF}", tags=['Accounts'])
async def get_account(account_CPF:str):
#         /v1/accounts/12345678911
#         /v1/accounts/123.456.789-11
    """
    Method to return a single account, searching by CPF
    :path param: account_CPF - CPF from the register to return
    """
    account_CPF = account_CPF.replace(".","").replace("-","").upper()

    response = database.get_account(account_CPF=account_CPF)
    return {'message':'Data returned', 'data': response}


@app.delete("/v1/accounts/{account_CPF}", tags=['Accounts'])
async def delete_account(account_CPF:str):
#            /delete/12345678911
#            /delete/123.456.789-11
    """
    Method to delete an account
    :param: account_CPF - CPF from the register of the database to delete
    """
    if database.get_CPF(account_CPF):
        account_CPF = account_CPF.replace(".","").replace("-","").upper()
        database.delete_account(account_CPF=account_CPF)
        return {"message": "Account deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@app.put("/v1/accounts", tags=['Accounts'])
async def update_account(account: database.Account):
#         /update
    """
    Method to update 'name' or 'BRL' from an account, select by 'CPF'
    :param: account - type(Account Model)
    """
    if account.CPF != "":
        try:
            database.update_account(account=account)
            return {"message": "Account updated"}
        except:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsuported object format")


@app.get("/v1/accounts/{account_CPF}/convert", tags=['Accounts'])
async def convert(account_CPF:str, quota: str = "" ):  
#         /v1/accounts/12345678911/convert
#         /v1/accounts/123.456.789-11/convert?quota=BRL
    """
    Method to get the money from an account and convert to other quoatas
        - if has no query parameters, return all convertions
        - you can search a single convertion adding "?quota={quota_name}"
    """

    url = "http://api.exchangeratesapi.io/v1/latest?access_key=ee694924a67ecd528d6cc2288d7cf245&format=2"    
    response = requests.get(url=url).json()

    saldo_BRL = database.get_saldo(account_CPF)
    valor_BRL = response["rates"]["BRL"]

    if quota == "":
        saldos = {}
        for key in response['rates'].keys():
            saldos[key] = ( response["rates"][key] * saldo_BRL ) / valor_BRL
        return saldos
    else:
        a= response["rates"][quota] * saldo_BRL / valor_BRL
        return {quota:a}

@app.get('/nic', tags=['Friends Endpoint'])
async def get_clima():
    """
    Method to get an someone else endpoint
    :param: ip - IP from the other device
    :param: port - Port of the aplication
    :param: route - the endpoint to get
    """

    url = 'http://10.21.56.27:8001/clima-completo/valinhos'

    response = requests.get(url=url).json()
    
    return {'message':'Data returned', 'data': response}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)