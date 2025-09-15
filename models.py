from sqlalchemy import Column, Integer, String, DECIMAL
from Model.conexaoDB import SessionLocal, Base, engine

# ORM de produto
class Produto(Base):
    __tablename__ = "Produtos"

    id = Column("idProduto", Integer, primary_key = True, nullable = False)
    nome = Column("Nome_Produto", String(100), nullable = False)
    preco = Column("Preço", DECIMAL, nullable = False)
    categoria = Column("Categoria", String(100), nullable = False)
    cor = Column("Cor", String(45), nullable = False)
    imagem = Column("Imagem", String(100), nullable=False)

Base.metadata.create_all(bind=engine)

# CREATE
def create(nome:str, preco:float, categoria:str, cor:str, imagem:str):
    session = SessionLocal()
    usuario=Produto(nome = nome, preco = preco, categoria = categoria, cor = cor, imagem = imagem)
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
def update(id_produto:int, novo_nome:str, novo_preco:float, nova_categoria:str, nova_cor:str, nova_imagem:str):
    session = SessionLocal()
    produto = session.query(Produto).filter(Produto.id==id_produto).first()
    if produto:
        produto.nome = novo_nome
        produto.preco = novo_preco
        produto.categoria = nova_categoria
        produto.cor = nova_cor
        produto.imagem = nova_imagem
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

