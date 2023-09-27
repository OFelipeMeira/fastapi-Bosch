import sqlite3
from pydantic import BaseModel
from typing import Optional
from prettytable import *

class Account(BaseModel):
    id: Optional[int] = None
    name:str
    BRL: float
    CPF: str

def setup_connection():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("Create Table Accounts ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, BRL DOUBLE, CPF TEXT );")

#def new_account(name: str, BRL: float):
def new_account(account:Account):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    filtered_CPF = account.CPF.replace(".","").replace("-","")
    cursor.execute(f"""Insert Into Accounts(name, BRL, CPF)
                   Values ( '{account.name}' , '{account.BRL}', '{filtered_CPF}')""")
    con.commit()
    con.close()

def get_accounts():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    resp = cursor.execute("SELECT * FROM Accounts").fetchall()
    con.close()
    return resp

def get_account(account_CPF:str):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    account_CPF = account_CPF.replace(".","").replace("-","").upper()
    resp = cursor.execute(f"SELECT * FROM Accounts WHERE CPF='{account_CPF}'").fetchone()
    con.close()
    return resp

def get_saldo(account_CPF:str):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    account_CPF = account_CPF.replace(".","").replace("-","").upper()
    resp = cursor.execute(f"SELECT BRL FROM Accounts WHERE id={account_CPF}").fetchone()[0]
    con.close()
    return resp

def update_account(account: Account):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    cursor.execute(f"UPDATE Accounts SET name='{account.name}', BRL={account.BRL}  WHERE id={account.id}")

    con.commit()
    con.close()

def delete_account(account_CPF:str):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    account_CPF = account_CPF.replace(".","").replace("-","").upper()
    cursor.execute(f"DELETE FROM Accounts WHERE CPF='{account_CPF}'")
    con.commit()
    con.close()

def print_data(table):
    x = PrettyTable()
    x.field_names = ["id", "name", "BRL", "CPF"]
    x.add_rows(table)
    print(x)


if __name__=="__main__":
    # setup_connection()
    
    print(get_accounts())

    # print_data( get_accounts() )
    # print( get_account("XXX.XXX.XXX-XX") )


