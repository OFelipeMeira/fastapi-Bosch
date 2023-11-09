from pydantic.v1 import BaseSettings

class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'

    DB_URL: str = 'mysql+asyncmy://root@127.0.0.1:3306/etscursos'

    class Config:
        case_sensitive = True

settings = Settings()