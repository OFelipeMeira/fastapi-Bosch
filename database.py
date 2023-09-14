import sqlite3
from pydantic import BaseModel

def setup_connection():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("""Create Table Accounts(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   BRL DOUBLE)""")
    return {"message": "Connection setted up"}

class Account(BaseModel):
    id:int
    name:str
    BRL: float

def new_account(name: str, BRL: float):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(f"""Insert Into Accounts(name, BRL)
                   Values ( '{name}' , '{BRL}')""")
    con.commit()
    con.close()
    return {"message": "Account added with success"}

def get_accounts():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    resp = cursor.execute("select * from Accounts").fetchall()
    con.close()
    return {"data": resp}

def update_account(account_id:int, new_name:str = "", new_BRL:float = ""):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    if new_name == "" and new_BRL=="":
        return {'ERROR': "No changes new values"}

    if new_name != "":
        print(f"{new_name}\n")
        #cursor.execute(f"UPDATE Accounts SET name={new_name} WHERE id={account_id}")
        cursor.execute(f"UPDATE Accounts SET name='{new_name}'  WHERE id={account_id}")
    if new_BRL != "":
        cursor.execute(f"UPDATE Accounts SET BRL ={new_BRL}  WHERE id={account_id}")

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
    # print( new_account("Bob Esponja", 40.0) )
    # print( update_account(1, new_BRL=100) )
    # print( update_account(1, new_name="abelardo") )
    # print( get_accounts() ) 
    print( delete_account(4) )
