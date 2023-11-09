"""
    Dependencies file
"""

# # To Test ------------------------------------------------------------------------- #
# import sys                                                                          #
# default_path = "C:\\Users\\CT67CA\\Desktop\\Temp Felipe DS6\\Python\\fastapi-Bosch" #
# sys.path.append(default_path)                                                       #
# # --------------------------------------------------------------------------------- # 

from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()