from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
#APIRouter = Rotas API para o front,
#request = Requisição HTTP, 
#Form = Formulário para criar e editar
#UploadFile = Upload da foto
#File = Função para gravar caminho da imagem
#Depends = Dependência do banco de dados sqlite #pip install python-multipart

from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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

from models import Produto, Usuario, ItemPedido, Pedido

from Model.auth import gerar_hash_senha, verificar_senha, criar_token, verificar_token

#Produto = Modelagem, nome, preço, quantidade, imagem

router = APIRouter() #Rotas
templates = Jinja2Templates(directory='./View/templates') #Front-end

# Caminho da pasta de uploads
UPLOAD_DIR = "static/uploads"  # sem a barra inicial

os.makedirs(UPLOAD_DIR, exist_ok=True)  # cria a pasta se não existir)

def verificando_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        return False
    
    payload = verificar_token(token)
    if not payload:
        return False
    
    return True

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
    payload = verificando_token(request)
    if payload:
        return RedirectResponse(url="/me/produtos", status_code=303)

    query = db.query(Produto) # consultar todos os produtos / economizar linha

    
    if categoria:
        query = query.filter(Produto.categoria == categoria) 
        #como o filter() ñ altera o obj query original a gnt temq armazenar na variável, senão será ignorado

    total_produtos = query.count()  # conta quantos produtos existem

    # Se o offset for maior ou igual ao total, volta pro início
    if offset >= total_produtos:
        offset = 0 # restarta offset

    produtos = query.offset(offset).limit(limit).all()

    # Calcula o próximo offset
    proximo_offset = offset + limit

    # Se o próximo offset passar do total, na próxima vez volta ao início
    if proximo_offset >= total_produtos:
        proximo_offset = 0

    if produtos:
        return templates.TemplateResponse('loja.html', {
            'request': request,
            'produtos': produtos,
            'categoria': categoria,
            'offset': proximo_offset,  # devolve o offset para o próximo clique
            'limit': limit
        })

#Rota para listar único produto
@router.get('/produto/{id_produto}', response_class=HTMLResponse)
async def detalhe(request:Request, id_produto:int, db:Session=Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    
    token = request.cookies.get("token")
    carrinho = []
    if token:
        payload = verificar_token(token)
        if payload:
            email_usuario = payload.get("sub")
            usuario = db.query(Usuario).filter(Usuario.email == email_usuario).first()
            carrinho = carrinhos.get(usuario.id, [])
    
    return templates.TemplateResponse('produto.html', {
        'request': request,
        'produto': produto,
        'carrinho': carrinho
    })

#Rota para mostrar página sobre
@router.get('/sobre', response_class=HTMLResponse)
async def listar_home(request:Request, db:Session = Depends(get_db)):
    return templates.TemplateResponse('sobre.html', {
        'request':request
    })

#Rota para mostrar página login
@router.get('/login', response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse('login.html', {
        'request':request
    })

# ----- Login -----

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return JSONResponse({"mensagem": "Usuário não encontrado."}, status_code=401)

    try:
        if not verificar_senha(senha, usuario.senha):
            return JSONResponse({"mensagem": "Senha incorreta."}, status_code=401)
    except Exception as e:
        print(f"Erro ao verificar senha para {email}: {e}")
        return JSONResponse({"mensagem": "Erro ao verificar senha. Tente redefinir sua senha."},status_code=500)

    if usuario.is_admin:
        token = criar_token({"sub": usuario.email, "is_admin": True})
        destino = "/admin"
    else:
        token = criar_token({"sub": usuario.email})
        destino = "/me/produtos"

    response = RedirectResponse(url=destino, status_code=302)
    response.set_cookie(key="token",value=token,httponly=True)
    return response

# -----   -----

# ----- User Produtos -----

@router.get('/me/produtos', response_class=HTMLResponse)
async def listar_produtos_user(request: Request, offset: int = 0, limit: int = 6, db: Session = Depends(get_db)):
    produtos = db.query(Produto).offset(offset).limit(limit).all()
    total_produtos = db.query(Produto).count()
    proximo_offset = offset + limit if offset + limit < total_produtos else 0

    return templates.TemplateResponse('loja-user.html', {
        'request': request,
        'produtos': produtos,
        'offset': proximo_offset,
        'limit': limit
    })

# -----   -----

# ----- Dados user -----
@router.get("/me/dados", response_class=HTMLResponse)
def listar_dados(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)
    
    email = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    return templates.TemplateResponse('dados.html', {
        'request': request,
        'user': usuario
    })
# -----   -----

# ----- User Pedidos -----

@router.get('/me/pedidos', response_class=HTMLResponse)
def listar_pedidos(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email_usuario = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email_usuario).first()
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    # Busca apenas os pedidos desse usuário
    pedidos = db.query(Pedido).filter(Pedido.id_usuario == usuario.id).all()

    return templates.TemplateResponse(
        'meus-pedidos.html',
        {'request': request, 'pedidos': pedidos}
    )

# -----   -----

#Rota para mostrar página cadastro
@router.get('/register', response_class=HTMLResponse)
async def cadastro(request:Request):
    return templates.TemplateResponse('cadastro.html', {
        'request':request
    })
@router.post('/register')
async def cadastrar_usuario(
    nome:str = Form(...),
    email:str = Form(...),
    senha:str = Form(...),
    db:Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {'mensagem':'E-mail já cadastrado'}
    else:
        senha_hash = gerar_hash_senha(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return RedirectResponse(url='/login', status_code=303)

#carrinho simples em memória
#adicionar itens ao carrinho
carrinhos={}
# rotas para carrinho 
@router.post("/carrinho/adicionar/{id_produto}")
async def adicionar_carrinho(
    request: Request,
    id_produto: int,
    quantidade: int = Form(1),
    db: Session = Depends(get_db)
):
    # para funcionar o usuário tem que estar logado
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    # caso contrário pega o email dele
    email_usuario = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email_usuario).first()
    produto = db.query(Produto).filter(Produto.id == id_produto).first()
    if not produto:
        return RedirectResponse(url="/", status_code=303)

    carrinho=carrinhos.get(usuario.id,[])
    if len(carrinho) >= 1:
        # se já houver item, redireciona direto para o carrinho
        return RedirectResponse(url="/carrinho", status_code=303)
    
    carrinho.append({
        "id":produto.id,
        "nome":produto.nome,
        "preco":float(produto.preco),
        "quantidade":quantidade
    })
    carrinhos[usuario.id]=carrinho # o id... fez tal pedido
    return RedirectResponse(url="/carrinho", status_code=303)

    # item_existente = db.query(Carrinho).filter(
    #     Carrinho.id_usuario == usuario.id,
    #     Carrinho.id_produto == produto.id
    # ).first()

    # if item_existente:
    #     item_existente.quantidade += quantidade
    # else:
    #     novo_item = Carrinho(id_usuario=usuario.id, id_produto=produto.id, quantidade=quantidade)
    #     db.add(novo_item)

    # db.commit()

# rota para visualizar o carrinho
@router.get("/carrinho", response_class=HTMLResponse)
async def ver_carrinho(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email_usuario = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email_usuario).first()
    carrinho=carrinhos.get(usuario.id,[])
    # itens = db.query(Carrinho).filter(Carrinho.id_usuario == usuario.id).all()
    total=round(sum(item["preco"]*item["quantidade"] for item in carrinho), 2)

    return templates.TemplateResponse("carrinho.html", {
        "request": request,
        "carrinho": carrinho,
        "total":total
    })

@router.post("/checkout")
async def checkout(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email_usuario = payload.get("sub")
    usuario = db.query(Usuario).filter(Usuario.email == email_usuario).first()
    carrinho = carrinhos.get(usuario.id, [])

    if not carrinho:
        return {"mensagem": "Carrinho vazio"}

    # calcula o total
    total = round(sum(item["preco"] * item["quantidade"] for item in carrinho), 2)

    # cria o pedido
    pedido = Pedido(id_usuario=usuario.id, total=total)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)  # para ter acesso ao pedido.id

    # adiciona os itens do carrinho na tabela ItemPedido
    for item in carrinho:
        novo_item = ItemPedido(
            id_pedido=pedido.id, 
            id_produto=item["id"],
            quantidade=item["quantidade"],
            preco_unitario=item["preco"]
        )
        db.add(novo_item)

    db.commit()

    # limpa o carrinho
    carrinhos[usuario.id] = []

    return RedirectResponse(url="/meus-pedidos", status_code=303)


#listar pedidos do usuário
@router.get("/meus-pedidos",response_class=HTMLResponse)
def meus_pedidos(request:Request,db:Session=Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    payload = verificar_token(token)
    if not payload:
        return RedirectResponse(url="/login", status_code=303)

    email_usuario = payload.get("sub")
    usuario=db.query(Usuario).filter_by(email=email_usuario).first()
    pedidos = db.query(Pedido).filter_by(id_usuario=usuario.id).all()
    
    total_geral = sum(p.total for p in pedidos)
    
    return templates.TemplateResponse("checkout.html",
                                      {"request":request, "pedidos":pedidos, "total_geral":total_geral})
    
@router.get("/api/contador-carrinho")
def contador_carrinho(db: Session = Depends(get_db), request: Request = None):
    token = request.cookies.get("token")
    payload = verificar_token(token)
    if not payload:
        return {"quantidade": 0}

    email = payload.get("sub")
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario:
        return {"quantidade": 0}

    # Contar todos os produtos nos pedidos desse usuário
    pedidos = db.query(Pedido).filter_by(id_usuario=usuario.id).all()

    quantidade_total = 0
    for pedido in pedidos:
        itens = db.query(ItemPedido).filter_by(id_pedido=pedido.id).all()
        quantidade_total += sum(i.quantidade for i in itens)

    return {"quantidade": quantidade_total}

# #rota para deletar o produto do carrinho
@router.post("/carrinho/remover/{id_item}")
async def remover_carrinho(request: Request, id_item: int, db: Session = Depends(get_db)):
    item = db.query(Pedido).filter(Pedido.id == id_item).first()
    if item:
        db.delete(item)
        db.commit()
        return RedirectResponse(url="/produtos", status_code=303)


# ----- Página Admin -----

@router.get("/admin")
def admin(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("admin.html", {"request": request})

# -----   -----

# ----- Página Admin Produto -----

@router.get('/admin/produto', response_class=HTMLResponse)
async def listar_admin(request:Request):
    return templates.TemplateResponse('admin-produto.html', {'request':request})

# -----   -----

# ----- Página Admin Produto Deletar -----

@router.get('/admin/produto-deletar', response_class=HTMLResponse)
async def listar_admin_produto_deletar(request:Request, db:Session=Depends(get_db)):
    produtos = db.query(Produto).all()
    return templates.TemplateResponse('admin-produto-deletar.html', {
        'request': request,
        'produtos': produtos
    })

# -----   -----
@router.post("/admin/produto")
def criar_produto(
    request:Request,
    nome:str=Form(...),
    preco:float=Form(...),
    quantidade:int=Form(...),
    categoria:str=Form(...),
    cor:str=Form(...),
    imagem:UploadFile=File(...),
    detalhe1: UploadFile | None = File(None),
    detalhe2: UploadFile | None = File(None),
    detalhe3: UploadFile | None = File(None),
    detalhe4: UploadFile | None = File(None),
    db:Session=Depends(get_db)
):
    # Gera caminho completo para salvar a imagem principal
    caminho_arquivo = os.path.join(UPLOAD_DIR, imagem.filename)

    # Salva o arquivo
    with open(caminho_arquivo, "wb") as arquivo:
        shutil.copyfileobj(imagem.file, arquivo)
        
    novo_produto = Produto(
        nome=nome,
        preco=preco,
        quantidade=quantidade,
        categoria=categoria,
        cor=cor,
        imagem=imagem.filename,
        detalhe1=detalhe1.filename if detalhe1 else "",
        detalhe2=detalhe2.filename if detalhe2 else "",
        detalhe3=detalhe3.filename if detalhe3 else "",
        detalhe4=detalhe4.filename if detalhe4 else ""
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return RedirectResponse(url="/admin/produto",status_code=303)

@router.post("/admin/produto-deletar/{id}")
def deletar_produto(id:int,db:Session=Depends(get_db)):
    produto=db.query(Produto).filter(Produto.id==id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return RedirectResponse(url="/admin/produto-deletar",status_code=303)

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/produtos", status_code=302)
    response.delete_cookie(key="token")
    return response