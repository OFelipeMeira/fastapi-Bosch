from fastapi import FastAPI
import uvicorn
import database
import requests

app = FastAPI()

""" WORKS """
@app.post("/register")
def create_account(account: database.Account):
    database.new_account(account.name, account.BRL)
    return {'message': f"Account {account.name} created"}

""" WORKS """
@app.get("/accounts")
def get_accounts():
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response['data']}

""" WORKS """
@app.get("/account/{account_id}")
def get_account(account_id:int ):
    response = database.get_account(account_id=account_id)
    return {'message':'Data returned', 'data': response['data']}

""" WORKS """
@app.put("/update")
def update_account(account: database.Account):

    if len(get_account(account.id)['data']) == 1:
        database.update_account(account=account)
        return {"message": "Account updated"}
    elif len(get_account(account.id)['data']) > 1:
        return {"error": "too many itens found"}
    return {'message': "Account id not found"}

""" WORKS """
@app.delete("/delete/{account_id}")
def delete_account(account_id:int):
    database.delete_account(account_id=account_id)
    return {"message": "Account deleted"}

""" NOT YET """
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