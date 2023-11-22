"""
    General Configs File
    Defining configs
"""

from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    """
        General configs
    """

    # inicial 'endpoint' - to not be hard coded
    API_V1_STR: str = '/api/v1'

    # connection string - in this case using root as user, don't need a password
    # SqlAlchemy template: dialect+driver://username:password@host:port/database
    DB_URL: str = 'mysql+asyncmy://root@127.0.0.1:3306/db_fastapi'
    
    # for all models inherit all resources from sqlalchemy
    DBBaseModel = declarative_base()

    # boa pratica sqlalchemy
    class Config:
        case_sensitive = True

settings = Settings()
# importing this file can have acces to all the configs