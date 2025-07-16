"""
Testes unitários para o módulo de Pacientes.
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
from models.paciente import Paciente, ResponsavelLegal
from models.clinica import Clinica

# Configuração do banco de dados de teste
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
    """Cria e limpa o banco de dados para os testes do módulo."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fornece uma sessão de banco de dados limpa para cada teste."""
    db = TestingSessionLocal()
    # Limpar tabelas
    db.query(ResponsavelLegal).delete()
    db.query(Paciente).delete()
    db.query(Usuario).delete()
    db.query(Perfil).delete()
    db.query(Clinica).delete()
    db.commit()
    yield db
    db.close()

@pytest.fixture(scope="function")
def authenticated_client(db_session):
    """Cria um cliente autenticado para os testes."""
    # Criar dados necessários
    clinica = Clinica(nome="Clínica de Teste Paciente")
    perfil = Perfil(nome="Recepcionista")
    db_session.add_all([clinica, perfil])
    db_session.commit()

    username = f"recepcionista_{uuid4().hex[:4]}"
    password = "password"
    
    # Usar a API para criar o usuário e obter o token
    user_data = {
        "nome_usuario": username,
        "nome_completo": "Recepcionista Teste",
        "senha": password,
        "perfil_id": perfil.perfil_id,
        "clinica_id": clinica.id
    }
    client.post("/api/v1/usuarios/", json=user_data)
    
    login_data = {"nome_usuario": username, "senha": password}
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Criar cliente autenticado
    auth_client = TestClient(app)
    auth_client.headers = {"Authorization": f"Bearer {token}"}
    
    return auth_client

class TestPacienteAPI:
    """Testes para os endpoints de Pacientes."""

    def test_criar_paciente_sucesso(self, authenticated_client):
        """Testa a criação de um novo paciente com sucesso."""
        paciente_data = {
            "nome": "João",
            "sobrenome": "da Silva",
            "data_nascimento": "1990-05-15",
            "sexo": "M",
            "telefone": f"1198765{uuid4().hex[:4]}",
            "email": f"joao.silva.{uuid4().hex[:6]}@example.com"
        }
        response = authenticated_client.post("/api/v1/pacientes/", json=paciente_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == paciente_data["nome"]
        assert data["email"] == paciente_data["email"]
        assert "paciente_id" in data

    def test_listar_pacientes(self, authenticated_client):
        """Testa a listagem de pacientes."""
        # Criar um paciente primeiro
        paciente_data = {
            "nome": "Maria", "sobrenome": "Souza", "data_nascimento": "1985-10-20",
            "email": f"maria.souza.{uuid4().hex[:6]}@example.com"
        }
        authenticated_client.post("/api/v1/pacientes/", json=paciente_data)

        response = authenticated_client.get("/api/v1/pacientes/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["nome"] == "Maria"

    def test_obter_paciente_por_id(self, authenticated_client):
        """Testa a busca de um paciente específico pelo seu ID."""
        paciente_data = {
            "nome": "Carlos", "sobrenome": "Pereira", "data_nascimento": "2000-01-01",
            "email": f"carlos.pereira.{uuid4().hex[:6]}@example.com"
        }
        create_response = authenticated_client.post("/api/v1/pacientes/", json=paciente_data)
        paciente_id = create_response.json()["paciente_id"]

        response = authenticated_client.get(f"/api/v1/pacientes/{paciente_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["paciente_id"] == paciente_id
        assert data["nome"] == "Carlos"

    def test_adicionar_responsavel_legal(self, authenticated_client):
        """Testa adicionar um responsável legal a um paciente."""
        paciente_data = {
            "nome": "Ana", "sobrenome": "Lima", "data_nascimento": "2015-03-10", # Menor de idade
            "email": f"ana.lima.{uuid4().hex[:6]}@example.com"
        }
        create_response = authenticated_client.post("/api/v1/pacientes/", json=paciente_data)
        paciente_id = create_response.json()["paciente_id"]

        responsavel_data = {
            "nome": "Marcos Lima",
            "cpf": f"111.222.333-{uuid4().hex[:2]}",
            "grau_parentesco": "Pai"
        }
        
        response = authenticated_client.post(f"/api/v1/pacientes/{paciente_id}/responsaveis", json=responsavel_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == responsavel_data["nome"]
        assert data["paciente_id"] == paciente_id

    def test_paciente_nao_encontrado(self, authenticated_client):
        """Testa a resposta para um paciente que não existe."""
        paciente_id = uuid4()
        response = authenticated_client.get(f"/api/v1/pacientes/{paciente_id}")
        assert response.status_code == 404
