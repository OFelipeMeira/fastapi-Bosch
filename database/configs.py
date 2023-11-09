from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="mysql://root@127.0.0.1:3306/etscursos",
        modules={ 'models': ['database.models'] }
    )
    await Tortoise.generate_schemas()

async def connect():
    await Tortoise.init(
        db_url="mysql://root@127.0.0.1:3306/etscursos",
        modules={ 'models': ['database.models'] }
    )

async def disconnect():
    await Tortoise.close_connections()