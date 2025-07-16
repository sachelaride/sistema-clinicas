"""
Testes unitários para o módulo de Agendamento.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime, timedelta, time

from main import app
from database.base import Base
from database.session import get_db
from models.usuario import Usuario, Perfil
from models.clinica import Clinica
from models.paciente import Paciente
from models.agendamento import Agendamento, Sala, Servico, HorarioDisponibilidade, StatusAgendamento, DiaSemana

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
    """Cria e limpa o banco de dados para os testes do módulo."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fornece uma sessão de banco de dados limpa para cada teste."""
    db = TestingSessionLocal()
    # Limpar tabelas relevantes antes de cada teste
    db.query(Agendamento).delete()
    db.query(HorarioDisponibilidade).delete()
    db.query(Servico).delete()
    db.query(Sala).delete()
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
    clinica = Clinica(nome="Clínica de Teste Agendamento")
    perfil_atendente = Perfil(nome="Recepcionista")
    perfil_profissional = Perfil(nome="Profissional")
    db_session.add_all([clinica, perfil_atendente, perfil_profissional])
    db_session.commit()
    db_session.refresh(clinica)
    db_session.refresh(perfil_atendente)
    db_session.refresh(perfil_profissional)

    username = f"atendente_{uuid4().hex[:4]}"
    password = "password"
    
    # Usar a API para criar o usuário e obter o token
    user_data = {
        "nome_usuario": username,
        "nome_completo": "Atendente Teste",
        "senha": password,
        "perfil_id": perfil_atendente.perfil_id,
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
    auth_client.user_id = login_response.json()["usuario"]["usuario_id"]
    auth_client.perfil_profissional_id = perfil_profissional.perfil_id
    
    return auth_client

@pytest.fixture(scope="function")
def paciente_teste(db_session):
    """Cria um paciente para ser usado nos testes de agendamento."""
    paciente = Paciente(
        paciente_id=uuid4(),
        nome="Paciente Agendamento",
        sobrenome="Teste",
        data_nascimento="1990-01-01",
        sexo="F",
        telefone="11999992222",
        email=f"paciente.agendamento.{uuid4().hex[:6]}@example.com"
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente

@pytest.fixture(scope="function")
def profissional_teste(db_session, authenticated_client):
    """Cria um profissional para ser usado nos testes de agendamento."""
    username = f"profissional_{uuid4().hex[:4]}"
    password = "password"
    user_data = {
        "nome_usuario": username,
        "nome_completo": "Profissional Agendamento",
        "senha": password,
        "perfil_id": authenticated_client.perfil_profissional_id,
        "clinica_id": authenticated_client.clinica_id
    }
    response = client.post("/api/v1/usuarios/", json=user_data)
    return response.json()["usuario_id"]

class TestAgendamentoAPI:
    """Testes para os endpoints de Agendamento."""

    def test_criar_sala_sucesso(self, authenticated_client):
        """Testa a criação de uma nova sala com sucesso."""
        sala_data = {
            "nome": "Consultório 1",
            "clinica_id": authenticated_client.clinica_id,
            "tipo": "Consultório"
        }
        response = authenticated_client.post("/api/v1/agendamento/salas", json=sala_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == sala_data["nome"]
        assert data["clinica_id"] == sala_data["clinica_id"]
        assert "id" in data

    def test_listar_salas_por_clinica(self, authenticated_client):
        """Testa a listagem de salas por clínica."""
        sala_data = {
            "nome": "Sala de Exames",
            "clinica_id": authenticated_client.clinica_id,
            "tipo": "Exames"
        }
        authenticated_client.post("/api/v1/agendamento/salas", json=sala_data)

        response = authenticated_client.get(f"/api/v1/agendamento/salas/clinica/{authenticated_client.clinica_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(s["nome"] == "Sala de Exames" for s in data)

    def test_criar_servico_sucesso(self, authenticated_client):
        """Testa a criação de um novo serviço com sucesso."""
        servico_data = {
            "nome": "Limpeza Dental",
            "clinica_id": authenticated_client.clinica_id,
            "duracao_media_minutos": 60,
            "descricao": "Limpeza e profilaxia"
        }
        response = authenticated_client.post("/api/v1/agendamento/servicos", json=servico_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == servico_data["nome"]
        assert data["clinica_id"] == servico_data["clinica_id"]
        assert "id" in data

    def test_listar_servicos_por_clinica(self, authenticated_client):
        """Testa a listagem de serviços por clínica."""
        servico_data = {
            "nome": "Consulta de Rotina",
            "clinica_id": authenticated_client.clinica_id,
            "duracao_media_minutos": 30
        }
        authenticated_client.post("/api/v1/agendamento/servicos", json=servico_data)

        response = authenticated_client.get(f"/api/v1/agendamento/servicos/clinica/{authenticated_client.clinica_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(s["nome"] == "Consulta de Rotina" for s in data)

    def test_criar_horario_disponibilidade_sucesso(self, authenticated_client, profissional_teste):
        """Testa a criação de um horário de disponibilidade para um profissional."""
        horario_data = {
            "usuario_id": profissional_teste,
            "dia_semana": DiaSemana.SEGUNDA.value,
            "hora_inicio": "09:00:00",
            "hora_fim": "12:00:00"
        }
        response = authenticated_client.post("/api/v1/agendamento/disponibilidade", json=horario_data)
        assert response.status_code == 200
        data = response.json()
        assert data["usuario_id"] == profissional_teste
        assert data["dia_semana"] == DiaSemana.SEGUNDA.value
        assert "id" in data

    def test_criar_agendamento_sucesso(self, authenticated_client, paciente_teste, profissional_teste, db_session):
        """Testa a criação de um novo agendamento."""
        # Criar sala e serviço
        sala = Sala(nome="Sala Agendamento", clinica_id=authenticated_client.clinica_id)
        servico = Servico(nome="Servico Agendamento", clinica_id=authenticated_client.clinica_id, duracao_media_minutos=30)
        db_session.add_all([sala, servico])
        db_session.commit()
        db_session.refresh(sala)
        db_session.refresh(servico)

        agendamento_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "profissional_id": profissional_teste,
            "sala_id": sala.id,
            "servico_id": servico.id,
            "data_hora_inicio": (datetime.now() + timedelta(days=1)).isoformat(),
            "data_hora_fim": (datetime.now() + timedelta(days=1, minutes=30)).isoformat()
        }
        response = authenticated_client.post("/api/v1/agendamento/", json=agendamento_data)
        assert response.status_code == 200
        data = response.json()
        assert data["paciente_id"] == agendamento_data["paciente_id"]
        assert data["profissional_id"] == agendamento_data["profissional_id"]
        assert data["clinica_id"] == authenticated_client.clinica_id
        assert data["status"] == StatusAgendamento.AGENDADO.value
        assert "id" in data

    def test_listar_agendamentos_calendario(self, authenticated_client, paciente_teste, profissional_teste, db_session):
        """Testa a listagem de agendamentos para o calendário."""
        # Criar sala e serviço
        sala = Sala(nome="Sala Calendario", clinica_id=authenticated_client.clinica_id)
        servico = Servico(nome="Servico Calendario", clinica_id=authenticated_client.clinica_id, duracao_media_minutos=30)
        db_session.add_all([sala, servico])
        db_session.commit()
        db_session.refresh(sala)
        db_session.refresh(servico)

        # Criar um agendamento para hoje
        now = datetime.now()
        agendamento_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "profissional_id": profissional_teste,
            "sala_id": sala.id,
            "servico_id": servico.id,
            "data_hora_inicio": now.isoformat(),
            "data_hora_fim": (now + timedelta(minutes=30)).isoformat()
        }
        authenticated_client.post("/api/v1/agendamento/", json=agendamento_data)

        # Buscar agendamentos para o período
        start_date = (now - timedelta(days=7)).isoformat()
        end_date = (now + timedelta(days=7)).isoformat()
        response = authenticated_client.get(f"/api/v1/agendamento/calendario?start={start_date}&end={end_date}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(a["paciente_id"] == str(paciente_teste.paciente_id) for a in data)

    def test_atualizar_agendamento_status(self, authenticated_client, paciente_teste, profissional_teste, db_session):
        """Testa a atualização do status de um agendamento."""
        # Criar sala e serviço
        sala = Sala(nome="Sala Update", clinica_id=authenticated_client.clinica_id)
        servico = Servico(nome="Servico Update", clinica_id=authenticated_client.clinica_id, duracao_media_minutos=30)
        db_session.add_all([sala, servico])
        db_session.commit()
        db_session.refresh(sala)
        db_session.refresh(servico)

        # Criar um agendamento
        agendamento_data = {
            "paciente_id": str(paciente_teste.paciente_id),
            "profissional_id": profissional_teste,
            "sala_id": sala.id,
            "servico_id": servico.id,
            "data_hora_inicio": (datetime.now() + timedelta(days=2)).isoformat(),
            "data_hora_fim": (datetime.now() + timedelta(days=2, minutes=30)).isoformat()
        }
        create_response = authenticated_client.post("/api/v1/agendamento/", json=agendamento_data)
        agendamento_id = create_response.json()["id"]

        # Atualizar status para CONFIRMADO
        update_data = {"status": StatusAgendamento.CONFIRMADO.value}
        response = authenticated_client.put(f"/api/v1/agendamento/{agendamento_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agendamento_id
        assert data["status"] == StatusAgendamento.CONFIRMADO.value
