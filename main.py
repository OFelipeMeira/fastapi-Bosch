# from fastapi import FastAPI
# # from core.configs import settings
# from api.v1._api import api_router

# app = FastAPI(title="API de Cursos da ETS")
# app.include_router(api_router, prefix=settings.API_V1_STR)

def api_deezer():
    import requests
    r = requests.get('https://api.deezer.com/search?q=nothing-else-metters')
    response = r.json()['data'] 

    # print(r.status_code)
    # print(response)
    arrIDs = []
    if (len(response)<=5):
        for i in range( len(response) ):
            print(f"[{i}]\t" + response[i]['title'] + ' by ' + response[i]['artist']['name'])
            arrIDs.append(response[i]['id'])
    else:
        for i in range( 5 ):
            print(f"[{i}]\t"+response[i]['title'] + ' by ' + response[i]['artist']['name'])
            arrIDs.append(response[i]['id'])

    number = int(input("digite a musica que vc quer buscar"))
    print("\n\n" +f'https://api.deezer.com/track/{arrIDs[number]}'+ "\n\n")
    r = requests.get(f'https://api.deezer.com/track/{arrIDs[number]}')
    response = r.json()
    print(response)


async def create_db():
    await configs.init()

if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
    from database import configs
    import asyncio

    asyncio.run(create_db())
    
