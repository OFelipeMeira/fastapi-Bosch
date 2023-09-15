from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import database
import requests
import json

app = FastAPI()

""" WORKS """
@app.post("/register")
def create_account(account: database.Account):
    if account:
        database.new_account(account=account)
        return {'message': f"Account {account.name} created"}
    else:
        return {'message': f"Account {account.name} not created"}

""" WORKS """
@app.get("/accounts")
def get_accounts():
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response}

""" WORKS """
@app.get("/account/{account_id}")
def get_account(account_id:int):
    response = database.get_account(account_id=account_id)
    return {'message':'Data returned', 'data': response}

""" WORKS """
@app.put("/update")
def update_account(account: database.Account):
    try:
        if database.get_account(account.id) != None:
            database.update_account(account=account)
            return {"message": "Account updated"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID não encontrado")
    
    except Exception as e:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formato do objecto não suportado")
        print(e)
        return e


""" WORKS """
@app.delete("/delete/{account_id}")
def delete_account(account_id:int):
    database.delete_account(account_id=account_id)
    return {"message": "Account deleted"}

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