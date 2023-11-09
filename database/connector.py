from tortoise import Tortoise
from core.configs import settings

async def init():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={ 'models': ['database.models'] }
    )
    await Tortoise.generate_schemas()

async def connect():
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={ 'models': ['database.models'] }
    )

async def disconnect():
    await Tortoise.close_connections()