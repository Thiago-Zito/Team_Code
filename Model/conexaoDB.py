from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from sqlalchemy.exc import SQLAlchemyError

# Criar engine e session
def get_engine_session():
    try:
        user = "root"
        password = "dev1t@24"
        database = "ecommerce"

        password = quote_plus(password)
        engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost:3306/{database}')
        conn = engine.connect()
        conn.close()
        
        SessionLocal = sessionmaker(bind=engine)
        return engine, SessionLocal
    except SQLAlchemyError as e:
        print("Falha ao conectar ao banco de dados!")
        print("Verifique as informações: user, password, database.")
        print(f"Erro: {e}")
        return None, None 

# Obter engine e SessionLocal
engine, SessionLocal = get_engine_session()

# Classe base para os models
Base = declarative_base()


#Função para dependência para injetar sessão no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        