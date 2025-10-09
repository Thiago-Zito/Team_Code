from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
#APIRouter = Rotas API para o front,
#request = Requisição HTTP, 
#Form = Formulário para criar e editar
#UploadFile = Upload da foto
#File = Função para gravar caminho da imagem
#Depends = Dependência do banco de dados sqlite #pip install python-multipart

from fastapi.responses import HTMLResponse, RedirectResponse
# HTMLResponse = Resposta do html, get, post, put, delete
#RedirectResponse = Redirecionar a resposta para o front

from fastapi.templating import Jinja2Templates
# Jinja2Templates = Responsável por renderizar o front-end

import os, shutil
# os = funções de sistema operacional,
# shutil = salva e puxa diretórios do sistema 'caminho das imagens'

from sqlalchemy.orm import Session
#Session = Modelgem do ORM models

from Model.conexaoDB import get_db, SessionLocal
#get_db = injeção do SessionLocal na API

from models import Produto

#Produto = Modelagem, nome, preço, quantidade, imagem

router = APIRouter() #Rotas
templates = Jinja2Templates(directory='./View/templates') #Front-end

# Pasta para salvar imagens
UPLOAD_DIR = './View/static/img'
#caminho para o os
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Rota para mostrar página home
@router.get('/', response_class=HTMLResponse)
async def listar_home(request:Request):
    #produtos = db.query(Produto).all() #Puxar produtos do banco de dados
    return templates.TemplateResponse('home.html', {
        'request':request
    })

# http://127.0.0.1:8000/produtos/?categoria=couro
#Rota para listar produtos na loja.html
@router.get('/produtos', response_class=HTMLResponse)
async def listar(request: Request, offset: int = 0, limit: int = 6, categoria: str = None, db: Session = Depends(get_db)):
    query = db.query(Produto) # consultar todos os produtos / economizar linha

    if categoria:
        query = query.filter(Produto.categoria == categoria) 
        #como o filter() ñ altera o obj query original a gnt temq armazenar na variável, senão será ignorado

    produtos = query.offset(offset).limit(limit).all()

    if produtos:
        return templates.TemplateResponse('loja.html', {
            'request': request, 'produtos': produtos, 'categoria': categoria, 'offset': offset, 'limit': limit})
    else:
        return HTMLResponse('<h2>Não há produtos nessa categoria.</h2>', status_code=200)

#Rota para listar único produto
@router.get('/produto/{id_produto}', response_class=HTMLResponse)
async def detalhe(request:Request, id_produto:int, db:Session=Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    
    return templates.TemplateResponse('produto.html', {
        'request':request, 'produto':produto
    })