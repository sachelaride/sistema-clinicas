"""
Testes unitários para o módulo de Usuários e Autenticação.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from main import app
from database.base import Base
from database.session import get_db
from models.usuario import Usuario, Perfil
from models.clinica import Clinica

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescrever a dependência do banco de dados
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db():
    """Fixture para criar e limpar o banco de dados para os testes do módulo."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture para fornecer uma sessão de banco de dados limpa para cada teste."""
    db = TestingSessionLocal()
    # Limpar tabelas relevantes antes de cada teste
    db.query(Usuario).delete()
    db.query(Perfil).delete()
    db.query(Clinica).delete()
    db.commit()
    yield db
    db.close()

@pytest.fixture(scope="function")
def test_data(db_session):
    """Fixture para criar dados básicos necessários para os testes."""
    # Criar clínica
    clinica = Clinica(nome="Clínica Teste Usuário", ativo=True)
    db_session.add(clinica)
    db_session.commit()
    db_session.refresh(clinica)

    # Criar perfil
    perfil = Perfil(nome="Atendente")
    db_session.add(perfil)
    db_session.commit()
    db_session.refresh(perfil)

    return {"clinica_id": clinica.id, "perfil_id": perfil.perfil_id}

class TestUsuarioAPI:
    """Testes para os endpoints de Usuários."""

    def test_criar_usuario_sucesso(self, test_data):
        """Testa a criação de um novo usuário com sucesso."""
        user_data = {
            "nome_usuario": f"testuser_{uuid4().hex[:6]}",
            "nome_completo": "Usuário de Teste",
            "senha": "senha123",
            "perfil_id": test_data["perfil_id"],
            "clinica_id": test_data["clinica_id"],
            "email": f"test_{uuid4().hex[:6]}@example.com"
        }
        response = client.post("/api/v1/usuarios/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome_usuario"] == user_data["nome_usuario"]
        assert data["email"] == user_data["email"]
        assert data["clinica"]["id"] == test_data["clinica_id"]

    def test_criar_usuario_nome_duplicado(self, test_data):
        """Testa a falha ao criar um usuário com nome de usuário que já existe."""
        user_data = {
            "nome_usuario": "usuario_duplicado",
            "nome_completo": "Usuário de Teste 1",
            "senha": "senha123",
            "perfil_id": test_data["perfil_id"],
            "clinica_id": test_data["clinica_id"]
        }
        # Primeira criação (deve ter sucesso)
        response1 = client.post("/api/v1/usuarios/", json=user_data)
        assert response1.status_code == 201

        # Segunda criação (deve falhar)
        user_data_2 = user_data.copy()
        user_data_2["nome_completo"] = "Usuário de Teste 2"
        response2 = client.post("/api/v1/usuarios/", json=user_data_2)
        assert response2.status_code == 400
        assert "Nome de usuário já existe" in response2.json()["detail"]

    def test_criar_usuario_sem_clinica(self, test_data):
        """Testa a criação de um usuário sem uma clínica (deve ser permitido para admin geral)."""
        user_data = {
            "nome_usuario": f"admin_{uuid4().hex[:6]}",
            "nome_completo": "Admin Geral",
            "senha": "senha123",
            "perfil_id": test_data["perfil_id"],
            "clinica_id": None
        }
        response = client.post("/api/v1/usuarios/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["clinica"] is None

    def test_login_sucesso(self, test_data):
        """Testa o login de um usuário com credenciais corretas."""
        username = f"login_user_{uuid4().hex[:6]}"
        password = "senha_segura"
        user_data = {
            "nome_usuario": username,
            "nome_completo": "Usuário para Login",
            "senha": password,
            "perfil_id": test_data["perfil_id"],
            "clinica_id": test_data["clinica_id"]
        }
        client.post("/api/v1/usuarios/", json=user_data)

        login_data = {"nome_usuario": username, "senha": password}
        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["usuario"]["nome_usuario"] == username

    def test_login_senha_incorreta(self, test_data):
        """Testa a falha de login com senha incorreta."""
        username = f"login_fail_{uuid4().hex[:6]}"
        password = "senha_correta"
        user_data = {
            "nome_usuario": username,
            "nome_completo": "Usuário para Falha de Login",
            "senha": password,
            "perfil_id": test_data["perfil_id"],
            "clinica_id": test_data["clinica_id"]
        }
        client.post("/api/v1/usuarios/", json=user_data)

        login_data = {"nome_usuario": username, "senha": "senha_errada"}
        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
        assert "Nome de usuário ou senha incorretos" in response.json()["detail"]

    def test_obter_usuario_me(self, test_data):
        """Testa o endpoint /me para obter dados do usuário logado."""
        username = f"me_user_{uuid4().hex[:6]}"
        password = "senha123"
        user_data = {
            "nome_usuario": username,
            "nome_completo": "Usuário Logado",
            "senha": password,
            "perfil_id": test_data["perfil_id"],
            "clinica_id": test_data["clinica_id"]
        }
        client.post("/api/v1/usuarios/", json=user_data)

        login_response = client.post("/api/v1/auth/login", data={"nome_usuario": username, "senha": password})
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/v1/usuarios/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["nome_usuario"] == username
