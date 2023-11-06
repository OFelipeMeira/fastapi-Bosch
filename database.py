
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import *
import pymysql

engine = db.create_engine('mysql+pymysql://root:shelvi31@127.0.0.1/errors?host=localhost?port=3306')
connection = engine.connect()
print(engine.table_names())