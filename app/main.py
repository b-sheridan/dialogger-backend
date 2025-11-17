from fastapi import FastAPI

from app.routers import titles

app = FastAPI()

app.include_router(titles.router, prefix='/titles', tags=['titles'])


@app.get('/health')
def health():
    return {'status': 'ok'}
