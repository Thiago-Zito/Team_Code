from fastapi import FastAPI
from controllers import router
from fastapi.staticfiles import StaticFiles # Montar pasta de imagem

app = FastAPI()
app.mount('/static', StaticFiles(directory='View/static'), name='static')

app.include_router(router)