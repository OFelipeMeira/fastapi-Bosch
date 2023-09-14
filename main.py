from fastapi import FastAPI
import uvicorn
import database

app = FastAPI()

@app.get("/")
def root():
    return {'message':"aopa"}

@app.post("/register")
def create_account(account: database.Account):
    database.new_account(account.name, account.BRL)
    return {'message': f"{account.name} created"}

@app.get("/accounts")
def get_accounts():
    response = database.get_accounts()
    return {'message':'Data returned', 'data': response['data']}

@app.put("/update/{account_id}")
def update_account(account_id:int, newName:str = "", newBRL: float =""):
    database.update_account(account_id=account_id,new_name= newName, new_BRL=newBRL)
    return {"message": "Account updated", "newValues":[newName, newBRL]}

@app.delete("/delete/{account_id}")
def delete_account(account_id:int):
    database.delete_account(account_id=account_id)
    return {"message": "Account deleted"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)