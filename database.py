import sqlite3
from pydantic import BaseModel
from typing import Optional

def setup_connection():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("Create Table Accounts ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, BRL DOUBLE );")
    return {"message": "Connection setted up"}

class Account(BaseModel):
    id: Optional[int] = None
    name:str
    BRL: float

#def new_account(name: str, BRL: float):
def new_account(account:Account):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(f"""Insert Into Accounts(name, BRL)
                   Values ( '{account.name}' , '{account.BRL}')""")
    con.commit()
    con.close()
    return {"message": "Account added with success"}

def get_accounts():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    resp = cursor.execute("SELECT * FROM Accounts").fetchall()
    con.close()
    return resp

def get_account(account_id:int):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    resp = cursor.execute(f"SELECT * FROM Accounts WHERE id={account_id}").fetchone()
    con.close()
    return resp

def get_saldo(account_id:int):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    resp = cursor.execute(f"SELECT BRL FROM Accounts WHERE id={account_id}").fetchone()[0]
    con.close()
    return resp

def update_account(account: Account):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    cursor.execute(f"UPDATE Accounts SET name='{account.name}', BRL={account.BRL}  WHERE id={account.id}")

    con.commit()
    con.close()
    return {"message": "Account Updated"}

def delete_account(account_id:int):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM Accounts WHERE id={account_id}")
    con.commit()
    con.close()
    return {"message":{f"Account deleted "}}

if __name__ == '__main__':
    # print( setup_connection() )
    
    # print( new_account("Bo Besponja", 40.4) )
    # print( new_account("Patrick Trela", 30.6) )
    # print( update_account(1, new_BRL=100) )
    # print( update_account(1, new_name="abelardo", new_BRL=15.5) )
    # print( delete_account(2) )

    # print( get_account(31234) )

    # get all accounts:
    #for account in get_accounts()["data"]:
    #   print(account)

    # a  = get_account(1)["data"]
    # print(len(a))

    newAccount = {
        'name': "AAAA",
        "BRL": 91
    }

    print( type(newAccount) )

    
    pass

