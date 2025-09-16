from fastapi import FastAPI

app=FastAPI(title="API Produtos")

produtos = {
    1: {
        "Produto": "Iphone",
        "Categoria": "Celular",
        "Descrição": "Celular de última geração",
        "Preço": 1800.0
    },
    2: {
        "Produto": "Samsung Galaxy S21",
        "Categoria": "Celular",
        "Descrição": "Smartphone Android com câmera de alta resolução",
        "Preço": 1500.0
    },
    3: {
        "Produto": "Notebook Dell Inspiron",
        "Categoria": "Informática",
        "Descrição": "Notebook com processador i5 e SSD de 512GB",
        "Preço": 2800.0
    },
    4: {
        "Produto": "Smart TV LG 50''",
        "Categoria": "Eletrônicos",
        "Descrição": "Televisão 4K com acesso a aplicativos",
        "Preço": 2200.0
    },
    5: {
        "Produto": "Fone de Ouvido JBL",
        "Categoria": "Áudio",
        "Descrição": "Fone Bluetooth com cancelamento de ruído",
        "Preço": 350.0
    },
    6: {
        "Produto": "Teclado Mecânico Redragon",
        "Categoria": "Informática",
        "Descrição": "Teclado gamer com LED RGB",
        "Preço": 280.0
    },
    7: {
        "Produto": "Mouse Logitech MX Master 3",
        "Categoria": "Informática",
        "Descrição": "Mouse ergonômico sem fio com alta precisão",
        "Preço": 450.0
    },
    8: {
        "Produto": "Geladeira Brastemp Frost Free",
        "Categoria": "Eletrodomésticos",
        "Descrição": "Refrigerador com capacidade de 400L",
        "Preço": 3200.0
    },
    9: {
        "Produto": "Ar Condicionado Split Samsung 12000 BTUs",
        "Categoria": "Eletrodomésticos",
        "Descrição": "Ar condicionado inverter com economia de energia",
        "Preço": 2400.0
    },
    10: {
        "Produto": "Alexa Echo Dot 5ª Geração",
        "Categoria": "Smart Home",
        "Descrição": "Assistente virtual com comando de voz",
        "Preço": 349.0
    },
    11: {
        "Produto": "Cafeteira Nespresso Inissia",
        "Categoria": "Eletroportáteis",
        "Descrição": "Máquina de café expresso com cápsulas",
        "Preço": 390.0
    },
    12: {
        "Produto": "PlayStation 5",
        "Categoria": "Games",
        "Descrição": "Console de nova geração da Sony",
        "Preço": 4500.0
    },
    13: {
        "Produto": "Xbox Series S",
        "Categoria": "Games",
        "Descrição": "Console compacto com suporte para jogos digitais",
        "Preço": 2800.0
    },
    14: {
        "Produto": "Monitor LG Ultrawide 29''",
        "Categoria": "Informática",
        "Descrição": "Monitor com resolução Full HD e tela ultrawide",
        "Preço": 1200.0
    },
    15: {
        "Produto": "Impressora HP DeskJet Ink Advantage",
        "Categoria": "Informática",
        "Descrição": "Impressora multifuncional com Wi-Fi",
        "Preço": 499.0
    },
    16: {
        "Produto": "Câmera GoPro HERO11",
        "Categoria": "Fotografia",
        "Descrição": "Câmera de ação à prova d'água com vídeo 5.3K",
        "Preço": 2800.0
    }
}

@app.get('/')
async def geral_produtos():
    return produtos

@app.get('/get-produto/{id_produto}')
async def produto(id_produto:int):
    return produtos[id_produto]

# Query parameter = consulta
# http://site_api/get-produto/?id=1 
@app.get('/get-produto-categoria')
async def get_produto_categoria(categoria:str):
    #loop p/ rodar todos os dados e achar a categoria da pesquisa
    for i in produtos:
        if produtos[i]["Categoria"] == categoria:
            return produtos[i]
    return {"Dados":"Não foi encontrado o produto."}

#biblioteca de metadata para objetos criar e atualizar e deletar
from pydantic import BaseModel
class Produto(BaseModel):
    nome_produto:str
    categoria:str
    descricao:str
    preco:float
    
@app.post('/cadastrar-produto/{produto_id}')
async def cadastrar_produto(produto_id:int,produto:Produto):
    if produto_id in produtos:
        return {"ERRO":"Jogador já existe"}
    produtos[produto_id]=produto #vai criar o produto
    return produtos[produto_id]

from typing import Optional
class AtualizarProduto(BaseModel):
    # None, pois os dados vão ser inputados pelo user
    nome_produto: Optional[str]=None
    categoria: Optional[str]=None
    descricao: Optional[str]=None
    preco: Optional[float]=None

@app.put('/atualizar-produto/{produto_id}')
async def atualizar_produto(produto_id:int, produto:Produto):
    if produto_id not in produtos:
        return {"ERRO":"Produto ñ existe"}
    if (produto.nome_produto) != None and (produto.categoria) != None and (produto.descricao) != None and (produto.preco) != None: #if produto for diferente de vazio
        produtos[produto_id]["Produto"]=produto.nome_produto
    return produtos[produto_id]

@app.delete('/exclusao-produto/{produto_id}')
async def excluir_produto(produto_id:int):
    if produto_id not in produtos:
        return {"ERRO":"Jogador ñ existe"}
    del produtos[produto_id]
    return {"Mensagem":"produto excluído"}

# python -m uvicorn nome_da_api_sem_py:app --reload