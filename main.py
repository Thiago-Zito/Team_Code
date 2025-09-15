from fastapi import FastAPI
from controllers import router
from fastapi.staticfiles import StaticFiles # Montar pasta de imagem

app = FastAPI(title='MVC Produtos')
app.mount('/View/templates/img', StaticFiles(directory='./View/templates/img'), name='img')

app.include_router(router)