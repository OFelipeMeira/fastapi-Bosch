"""
    Creating a connection
"""

# To Test ------------------------------------------------------------------------- #
import sys                                                                          #
default_path = "C:\\Users\\CT67CA\\Desktop\\Temp Felipe DS6\\Python\\fastapi-Bosch" #
sys.path.append(default_path)                                                       #
# --------------------------------------------------------------------------------- #

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

# importing the settings object created on configs.py
# from .configs import settings
from core.configs import settings

# creating a connection with the database
engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind= engine
)