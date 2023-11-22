from fastapi import FastAPI
from core.configs import settings
from api.v1._api import api_router

# to create database
from criar_table import create_table

app = FastAPI(title="API de cotação de moedas")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    import asyncio

    asyncio.run(create_table())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)