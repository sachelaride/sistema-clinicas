import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from config.settings import settings
from database.base import Base
from models.usuario import Usuario
from core.security import verify_password

# Configurar o banco de dados
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_admin_user():
    db = SessionLocal()
    try:
        admin_user = db.query(Usuario).filter(Usuario.nome_usuario == "admin").first()
        
        if admin_user:
            print(f"Usuário 'admin' encontrado. ID: {admin_user.usuario_id}")
            print(f"Hash da senha: {admin_user.senha_hash}")
            
            # Tentar verificar a senha
            is_correct = verify_password("adminpass", admin_user.senha_hash)
            print(f"Senha 'adminpass' está correta? {is_correct}")
        else:
            print("Usuário 'admin' NÃO encontrado no banco de dados.")
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_user()
