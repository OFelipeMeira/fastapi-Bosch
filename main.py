from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import database
import requests
import json

app = FastAPI()

""" WORKS """
@app.get("/")
async def home():
    return {"message": "Hello Word"}

""" WORKS """
@app.post("/register")
async def create_account(account: database.Account):
    if account:
        database.new_account(account=account)
        return {'message': f"Account {account.name} created"}
    else:
        return {'message': f"Account {account.name} not created"}

""" WORKS """
@app.get("/accounts")
async def get_accounts():
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response}

""" WORKS """
@app.get("/account/{account_CPF}")
async def get_account(account_CPF:str):
    account_CPF = account_CPF.replace(".","").replace("-","").upper()

    response = database.get_account(account_CPF=account_CPF)
    return {'message':'Data returned', 'data': response}

""" WORKS """
@app.delete("/delete/{account_CPF}")
async def delete_account(account_CPF:str):
    account_CPF = account_CPF.replace(".","").replace("-","").upper()
    database.delete_account(account_CPF=account_CPF)
    return {"message": "Account deleted"}

""" SEMI WORKS """
""" PRECISA VERIFICAR SE TEM O ID NO BANCO"""
@app.put("/update")
async def update_account(account: database.Account):
    print(f"\033[91m 1 \033[00m")
    if account.id != None:
        print(f"\033[91m 2 \033[00m")
        try:
            print(f"\033[91m 3 \033[00m")
            list = database.get_accounts()
            print(list)
            database.update_account(account=account)
            return {"message": "Account updated"}
        except Exception as e:
            print(e)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Formato do objeto não suportado")

""" WORKS """
@app.get("/convert/{account_id}")
async def convert(account_id:int, quota: str = "" ):  

    url = "http://api.exchangeratesapi.io/v1/latest?access_key=ee694924a67ecd528d6cc2288d7cf245&format=2"    
    response = requests.get(url=url).json()

    saldo_BRL = database.get_saldo(account_id=account_id)
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