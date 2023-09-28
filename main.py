from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import database
import requests
import json

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello Word"}


@app.post("/register")
async def create_account(account: database.Account):
#         /register
    if account:
        database.new_account(account=account)
        return {'message': f"Account {account.name} created"}
    else:
        return {'message': f"Account not created"}


@app.get("/accounts")
async def get_accounts():
#         /accounts
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response}


@app.get("/account/{account_CPF}")
async def get_account(account_CPF:str):
#         /account/12345678911
#         /account/123.456.789-11
    account_CPF = account_CPF.replace(".","").replace("-","").upper()

    response = database.get_account(account_CPF=account_CPF)
    return {'message':'Data returned', 'data': response}


@app.delete("/delete/{account_CPF}")
async def delete_account(account_CPF:str):
#            /delete/12345678911
#            /delete/123.456.789-11
    account_CPF = account_CPF.replace(".","").replace("-","").upper()
    database.delete_account(account_CPF=account_CPF)
    return {"message": "Account deleted"}


@app.put("/update")
async def update_account(account: database.Account):
    if account.CPF != "":
        try:
            database.update_account(account=account)
            return {"message": "Account updated"}
        except:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Formato do objeto não suportado")


@app.get("/account/{account_CPF}/convert")
async def convert(account_CPF:str, quota: str = "" ):  
#         /account/12345678911/convert
#         /account/123.456.789-11/convert?quota=BRL

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

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)