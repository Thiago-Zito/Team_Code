from sqlalchemy import Column, Integer, String, DECIMAL
from Team_Code.Model.conexaoDB import SessionLocal, Base

# ORM de produto
class Produto(Base):
    __tablename__ = "Produto"

    id = Column("idProduto", Integer, primary_key = True, nullable = False)
    nome = Column("Nome_Produto", String(100), nullable = False)
    preco = Column("Preço", DECIMAL, nullable = False)
    categoria = Column("Categoria", String(100), nullable = False)
    cor = Column("Cor", String(45), nullable = False)

# CREATE
def create(nome:str, preco:float, categoria:str, cor:str):
    session = SessionLocal()
    usuario=Produto(nome = nome, preco = preco, categoria = categoria, cor = cor)
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
def update(id_produto:int, novo_nome:str, novo_preco:float, nova_categoria:str, nova_cor:str):
    session = SessionLocal()
    produto = session.query(Produto).filter(Produto.id==id_produto).first()
    if produto:
        produto.nome = novo_nome
        produto.preco = novo_preco
        produto.categoria = nova_categoria
        produto.cor = nova_cor
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



