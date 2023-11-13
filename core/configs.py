from pydantic.v1 import BaseSettings

class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'

    DB_URL: str = 'mysql://root@127.0.0.1:3307/mybank'

    class Config:
        case_sensitive = True

settings = Settings()