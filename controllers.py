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
UPLOAD_DIR = './View/templates/img'
#caminho para o os
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Rota para mostrar página home
@router.get('/', response_class=HTMLResponse)
async def listar_home(request:Request, db:Session = Depends(get_db)):
    #produtos = db.query(Produto).all() #Puxar produtos do banco de dados
    return templates.TemplateResponse('home.html', {
        'request':request
    })

#Rota para listar produtos na loja.html
@router.get('/produtos', response_class=HTMLResponse)
async def listar(request:Request, offset: int = 0, limit: int = 6, db:Session = Depends(get_db)):
    produtos = db.query(Produto).offset(offset).limit(limit).all() #Puxar produtos do banco de dados com um limite de 6 produtos por tela
    return templates.TemplateResponse('loja.html', {
        'request':request, 'produtos':produtos, "offset":offset, "limit": limit
    })

#Rota para listar único produto
@router.get('/produto/{id_produto}', response_class=HTMLResponse)
async def detalhe(request:Request, id_produto:int, db:Session=Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    return templates.TemplateResponse('produto.html', {
        'request':request, 'produto':produto
    })

# Rota 