from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy import text
from Model.conexaoDB import SessionLocal, Base, engine
from Model.auth import gerar_hash_senha

# ORM de produto
class Produto(Base):
    __tablename__ = "Produtos"
    id = Column("idProduto", Integer, primary_key = True, nullable = False)
    nome = Column("Nome_Produto", String(100), nullable = False)
    preco = Column("Preço", DECIMAL, nullable = False)
    quantidade = Column("quantidade", Integer, nullable=False)
    categoria = Column("Categoria", String(100), nullable = False)
    cor = Column("Cor", String(45), nullable = False)
    imagem = Column("Imagem", String(100), nullable=False)
    detalhe1 = Column("Detalhe1", String(100), nullable=False)
    detalhe2 = Column("Detalhe2", String(100), nullable=False)
    detalhe3 = Column("Detalhe3", String(100), nullable=False)
    detalhe4 = Column("Detalhe4", String(100), nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))
    email = Column(String(100), unique=True)
    senha = Column(String(200))
    is_admin = Column(Boolean, default=False)

    pedidos = relationship("Pedido", back_populates="usuario")

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id")) # id do usuário que está fazendo o pedido
    total = Column(Float, default=0.0) # total de pedidos

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "item_pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id"))
    id_produto = Column(Integer, ForeignKey("Produtos.idProduto"))
    quantidade = Column(Integer, default=1) 
    preco_unitario = Column(Float)

    pedido = relationship("Pedido", back_populates="itens")

# with engine.connect() as conexao:
#     conexao.execute(text(
#         'ALTER TABLE Produtos ADD COLUMN quantidade'))

# Criação das tabelas
# Base.metadata.create_all(bind=engine)

# Criação de tabela específica
# Usuario.__table__.create(bind=engine, checkfirst=True)

# CRUD PARA PRODUTOS
# CREATE
def create(nome:str, preco:float, categoria:str, cor:str, imagem:str, detalhe1:str, detalhe2:str, detalhe3:str, detalhe4:str):
    session = SessionLocal()
    usuario=Produto(nome=nome, preco=preco, categoria=categoria, cor=cor, imagem=imagem, detalhe1=detalhe1, detalhe2=detalhe2, detalhe3=detalhe3, detalhe4=detalhe4)
    session.add(usuario)
    session.commit()
    session.close()

# READ
def read():
    session = SessionLocal()
    produtos = session.query(Produto).all()
    session.close()
    return produtos

# UPDATE
def update(id_produto:int, novo_nome:str, novo_preco:float, nova_categoria:str, nova_cor:str, nova_imagem:str, novo_detalhe1:str, novo_detalhe2:str, novo_detalhe3:str, novo_detalhe4:str):
    session = SessionLocal()
    produto = session.query(Produto).filter(Produto.id==id_produto).first()
    if produto:
        produto.nome = novo_nome
        produto.preco = novo_preco
        produto.categoria = nova_categoria
        produto.cor = nova_cor
        produto.imagem = nova_imagem
        produto.detalhe1 = novo_detalhe1
        produto.detalhe2 = novo_detalhe2
        produto.detalhe3 = novo_detalhe3
        produto.detalhe4 = novo_detalhe4
        session.commit()
    session.close()

# DELETE
def delete(id_produto:int):
    session=SessionLocal()
    produto=session.query(Produto).filter(Produto.id==id_produto).first()
    if produto:
        session.delete(produto)
        session.commit()
    session.close()

# teste criar
# create("Bolsa Auxiliar",
# 7600.000,
# "Tote",
# "marrom",
# "louis-vuitton-bolsa-carryall-vibe-mm-1.avif",
# "louis-vuitton-bolsa-carryall-vibe3.avif",
# "louis-vuitton-bolsa-carryall-vibe3.avif",
# "louis-vuitton-bolsa-carryall-vibe3.avif",
# "louis-vuitton-bolsa-carryall-vibe3.avif")

# teste ler 
# produtos = read()
# print(produtos)

# teste atualizar
# update(5,
# "Bolsa Legítima",
# 3.14,
# "Church",
# "Azul",
# "louis-vuitton-bolsa-carryall-vibe1.avif",
# "louis-vuitton-bolsa-carryall-vibe2.avif",
# "louis-vuitton-bolsa-carryall-vibe2.avif",
# "louis-vuitton-bolsa-carryall-vibe2.avif",
# "louis-vuitton-bolsa-carryall-vibe2.avif")

# teste deletar
# delete(25)

# CRUD PARA USUARIOS 
# create
def create_usuario(nome:str, email:str, senha:str, is_admin:bool):
    session = SessionLocal()
    usuario=Usuario(nome=nome, email=email, senha=senha, is_admin=is_admin)
    session.add(usuario)
    session.commit()
    session.close()

# create_usuario("Fernando", "fernando@gmail.com", gerar_hash_senha("minhasenha123"), is_admin=True)