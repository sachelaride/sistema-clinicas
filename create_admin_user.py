import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from config.settings import settings
from database.base import Base
from models.usuario import Usuario, Perfil
from models.clinica import Clinica
from schemas.usuario import UsuarioCreate, PerfilCreate
from crud.usuario import crud_usuario, crud_perfil

def create_initial_admin_user():
    db = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(settings.DATABASE_URL))()
    try:
        # Criar uma clínica padrão se não existir (para associar o admin, se necessário)
        clinica = db.query(Clinica).filter(Clinica.nome == "Clinica Padrao").first()
        if not clinica:
            clinica = Clinica(nome="Clinica Padrao", descricao="Clinica criada para o admin inicial")
            db.add(clinica)
            db.commit()
            db.refresh(clinica)
            print(f"Clínica padrão criada: {clinica.nome} (ID: {clinica.id})")

        # Criar perfil de Administrador se não existir
        admin_profile = crud_perfil.get_by_nome(db, "Administrador")
        if not admin_profile:
            admin_profile = crud_perfil.create(db, PerfilCreate(nome="Administrador"))
            print(f"Perfil 'Administrador' criado: ID {admin_profile.perfil_id}")

        # Criar usuário administrador padrão se não existir
        existing_admin = crud_usuario.get_by_nome_usuario(db, "admin")
        if not existing_admin:
            admin_user_data = UsuarioCreate(
                nome_usuario="admin",
                senha="adminpass", # Senha padrão
                nome_completo="Administrador do Sistema",
                perfil_id=admin_profile.perfil_id,
                email="admin@clinicas.com",
                clinica_id=clinica.id # Associar à clínica padrão
            )
            new_admin = crud_usuario.create(db, admin_user_data)
            print(f"Usuário 'admin' criado com sucesso! ID: {new_admin.usuario_id}")
            print(f"Senha hashada: {new_admin.senha_hash}")
        else:
            print("Usuário 'admin' já existe no banco de dados.")
            print(f"ID: {existing_admin.usuario_id}")
            print(f"Senha hashada: {existing_admin.senha_hash}")

    except Exception as e:
        db.rollback()
        print(f"Ocorreu um erro ao criar o usuário admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin_user()
