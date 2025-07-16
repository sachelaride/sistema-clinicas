"""
Testes unitários para o módulo de Gestão de Filas.
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
from models.paciente import Paciente
from models.fila import GuicheAtendimento, FilaEspera, StatusFila, PrioridadeFila

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
    db.query(FilaEspera).delete()
    db.query(GuicheAtendimento).delete()
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
    clinica = Clinica(nome="Clínica de Teste Fila")
    perfil = Perfil(nome="Atendente")
    db_session.add_all([clinica, perfil])
    db_session.commit()
    db_session.refresh(clinica)
    db_session.refresh(perfil)

    username = f"atendente_{uuid4().hex[:4]}"
    password = "password"
    
    # Usar a API para criar o usuário e obter o token
    user_data = {
        "nome_usuario": username,
        "nome_completo": "Atendente Teste",
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
    auth_client.clinica_id = clinica.id # Adicionar clinica_id ao cliente para facilitar testes
    
    return auth_client

@pytest.fixture(scope="function")
def paciente_teste(db_session):
    """Cria um paciente para ser usado nos testes de fila."""
    paciente = Paciente(
        paciente_id=uuid4(),
        nome="Paciente Fila",
        sobrenome="Teste",
        data_nascimento="2000-01-01",
        sexo="M",
        telefone="11999998888",
        email=f"paciente.fila.{uuid4().hex[:6]}@example.com"
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente

class TestGuicheAtendimentoAPI:
    """Testes para os endpoints de Guichês de Atendimento."""

    def test_criar_guiche_sucesso(self, authenticated_client):
        """Testa a criação de um novo guichê de atendimento com sucesso."""
        guiche_data = {
            "nome": "Guichê 1",
            "clinica_id": authenticated_client.clinica_id,
            "descricao": "Recepção principal"
        }
        response = authenticated_client.post("/api/v1/fila/guiches", json=guiche_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == guiche_data["nome"]
        assert data["clinica_id"] == guiche_data["clinica_id"]
        assert "id" in data

    def test_listar_guiches_por_clinica(self, authenticated_client):
        """Testa a listagem de guichês por clínica."""
        guiche_data = {
            "nome": "Guichê 2",
            "clinica_id": authenticated_client.clinica_id,
            "descricao": "Consultório A"
        }
        authenticated_client.post("/api/v1/fila/guiches", json=guiche_data)

        response = authenticated_client.get(f"/api/v1/fila/guiches/clinica/{authenticated_client.clinica_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1 # Pode haver outros guichês criados por outros testes
        assert any(g["nome"] == "Guichê 2" for g in data)

class TestFilaEsperaAPI:
    """Testes para os endpoints da Fila de Espera."""

    def test_adicionar_paciente_fila_sucesso(self, authenticated_client, paciente_teste):
        """Testa a adição de um paciente à fila de espera."""
        fila_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "servico_id": None, # Pode ser nulo para fila geral
            "prioridade": PrioridadeFila.NORMAL.value
        }
        response = authenticated_client.post("/api/v1/fila/entrada", json=fila_data)
        assert response.status_code == 200
        data = response.json()
        assert data["paciente_id"] == str(paciente_teste.paciente_id)
        assert data["clinica_id"] == authenticated_client.clinica_id
        assert data["status"] == StatusFila.AGUARDANDO.value
        assert "id" in data

    def test_chamar_proximo_fila_sucesso(self, authenticated_client, paciente_teste, db_session):
        """Testa a chamada do próximo paciente da fila."""
        # Criar um guichê
        guiche_data = {
            "nome": "Guichê Chamada",
            "clinica_id": authenticated_client.clinica_id,
            "descricao": "Guichê para testes de chamada"
        }
        guiche_response = authenticated_client.post("/api/v1/fila/guiches", json=guiche_data)
        guiche_id = guiche_response.json()["id"]

        # Adicionar paciente à fila
        fila_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "servico_id": None,
            "prioridade": PrioridadeFila.NORMAL.value
        }
        authenticated_client.post("/api/v1/fila/entrada", json=fila_data)

        # Chamar o próximo paciente
        response = authenticated_client.post(f"/api/v1/fila/chamar-proximo?guiche_id={guiche_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["paciente_id"] == str(paciente_teste.paciente_id)
        assert data["status"] == StatusFila.EM_ATENDIMENTO.value
        assert data["guiche_id"] == guiche_id
        assert "hora_chamada" in data

    def test_chamar_proximo_fila_vazia(self, authenticated_client):
        """Testa a chamada do próximo paciente quando a fila está vazia."""
        # Criar um guichê
        guiche_data = {
            "nome": "Guichê Vazio",
            "clinica_id": authenticated_client.clinica_id,
            "descricao": "Guichê para testes de fila vazia"
        }
        guiche_response = authenticated_client.post("/api/v1/fila/guiches", json=guiche_data)
        guiche_id = guiche_response.json()["id"]

        response = authenticated_client.post(f"/api/v1/fila/chamar-proximo?guiche_id={guiche_id}")
        assert response.status_code == 404
        assert "Nenhum paciente aguardando na fila." in response.json()["detail"]

    def test_atualizar_status_fila(self, authenticated_client, paciente_teste, db_session):
        """Testa a atualização do status de um item na fila."""
        # Adicionar paciente à fila
        fila_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "servico_id": None,
            "prioridade": PrioridadeFila.NORMAL.value
        }
        add_response = authenticated_client.post("/api/v1/fila/entrada", json=fila_data)
        fila_id = add_response.json()["id"]

        # Atualizar status para ATENDIDO
        update_data = {"status": StatusFila.ATENDIDO.value}
        response = authenticated_client.patch(f"/api/v1/fila/{fila_id}/status", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == fila_id
        assert data["status"] == StatusFila.ATENDIDO.value

    def test_listar_fila_por_status(self, authenticated_client, paciente_teste, db_session):
        """Testa a listagem da fila filtrando por status."""
        # Adicionar paciente AGUARDANDO
        fila_data_aguardando = {
            "paciente_id": str(paciente_teste.paciente_id),
            "servico_id": None,
            "prioridade": PrioridadeFila.NORMAL.value
        }
        authenticated_client.post("/api/v1/fila/entrada", json=fila_data_aguardando)

        # Criar outro paciente e adicionar EM_ATENDIMENTO
        paciente_em_atendimento = Paciente(
            paciente_id=uuid4(),
            nome="Paciente Em Atendimento",
            sobrenome="Teste",
            data_nascimento="1995-05-05",
            sexo="F",
            telefone="11999997777",
            email=f"paciente.atendimento.{uuid4().hex[:6]}@example.com"
        )
        db_session.add(paciente_em_atendimento)
        db_session.commit()
        db_session.refresh(paciente_em_atendimento)

        fila_data_em_atendimento = {
            "paciente_id": str(paciente_em_atendimento.paciente_id),
            "servico_id": None,
            "prioridade": PrioridadeFila.NORMAL.value
        }
        add_response_em_atendimento = authenticated_client.post("/api/v1/fila/entrada", json=fila_data_em_atendimento)
        fila_id_em_atendimento = add_response_em_atendimento.json()["id"]
        authenticated_client.patch(f"/api/v1/fila/{fila_id_em_atendimento}/status", json={"status": StatusFila.EM_ATENDIMENTO.value})

        # Listar apenas AGUARDANDO
        response_aguardando = authenticated_client.get(f"/api/v1/fila/clinica/{authenticated_client.clinica_id}?status={StatusFila.AGUARDANDO.value}")
        assert response_aguardando.status_code == 200
        data_aguardando = response_aguardando.json()
        assert len(data_aguardando) >= 1
        assert all(item["status"] == StatusFila.AGUARDANDO.value for item in data_aguardando)
        assert any(item["paciente_id"] == str(paciente_teste.paciente_id) for item in data_aguardando)

        # Listar apenas EM_ATENDIMENTO
        response_em_atendimento = authenticated_client.get(f"/api/v1/fila/clinica/{authenticated_client.clinica_id}?status={StatusFila.EM_ATENDIMENTO.value}")
        assert response_em_atendimento.status_code == 200
        data_em_atendimento = response_em_atendimento.json()
        assert len(data_em_atendimento) >= 1
        assert all(item["status"] == StatusFila.EM_ATENDIMENTO.value for item in data_em_atendimento)
        assert any(item["paciente_id"] == str(paciente_em_atendimento.paciente_id) for item in data_em_atendimento)
