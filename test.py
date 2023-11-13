# from database.models import Person
from database import connector
from database.models import *
import asyncio

async def init():
    # Creating tables
    print(await connector.init())

# async def create_account():
#     print( await models.Account.create()) 

async def get_accounts():
    await connector.connect()
    print(await Account.all())
    await connector.disconnect()


async def create_account():
    await connector.connect()
    await Account.create()

if __name__ == "__main__":

    account = {
        "name": "ACcount",
        "cpf": "12312312311"
    }

    MyModel.parse_obj

    # asyncio.run(init())
    asyncio.run(get_accounts())
    # asyncio.get_event_loop().run_until_complete(get_accounts())
