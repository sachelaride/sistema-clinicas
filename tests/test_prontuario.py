"""
Testes unitários para o módulo de Prontuário Eletrônico.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime

from main import app
from database.base import Base
from database.session import get_db
from models.usuario import Usuario, Perfil
from models.clinica import Clinica
from models.paciente import Paciente
from models.prontuario import Prontuario, Evolucao, AnexoProntuario, TipoAnexo
from models.agendamento import Agendamento, Sala, Servico, StatusAgendamento

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
    db.query(AnexoProntuario).delete()
    db.query(Evolucao).delete()
    db.query(Prontuario).delete()
    db.query(Agendamento).delete()
    db.query(Sala).delete()
    db.query(Servico).delete()
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
    clinica = Clinica(nome="Clínica de Teste Prontuario")
    perfil_profissional = Perfil(nome="Profissional")
    db_session.add_all([clinica, perfil_profissional])
    db_session.commit()
    db_session.refresh(clinica)
    db_session.refresh(perfil_profissional)

    username = f"profissional_{uuid4().hex[:4]}"
    password = "password"
    
    # Usar a API para criar o usuário e obter o token
    user_data = {
        "nome_usuario": username,
        "nome_completo": "Profissional Teste",
        "senha": password,
        "perfil_id": perfil_profissional.perfil_id,
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
    
    return auth_client

@pytest.fixture(scope="function")
def paciente_teste(db_session):
    """Cria um paciente para ser usado nos testes de prontuário."""
    paciente = Paciente(
        paciente_id=uuid4(),
        nome="Paciente Prontuario",
        sobrenome="Teste",
        data_nascimento="1990-01-01",
        sexo="F",
        telefone="11999991111",
        email=f"paciente.prontuario.{uuid4().hex[:6]}@example.com"
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente

@pytest.fixture(scope="function")
def agendamento_teste(db_session, paciente_teste, authenticated_client):
    """Cria um agendamento para ser associado a uma evolução."""
    clinica = db_session.query(Clinica).filter_by(id=authenticated_client.clinica_id).first()
    sala = Sala(nome="Sala Teste", clinica_id=clinica.id)
    servico = Servico(nome="Servico Teste", clinica_id=clinica.id, duracao_media_minutos=30)
    db_session.add_all([sala, servico])
    db_session.commit()
    db_session.refresh(sala)
    db_session.refresh(servico)

    agendamento = Agendamento(
        id=uuid4(),
        paciente_id=paciente_teste.paciente_id,
        profissional_id=UUID(authenticated_client.user_id),
        sala_id=sala.id,
        servico_id=servico.id,
        clinica_id=clinica.id,
        data_hora_inicio=datetime.now(),
        data_hora_fim=datetime.now(),
        status=StatusAgendamento.REALIZADO
    )
    db_session.add(agendamento)
    db_session.commit()
    db_session.refresh(agendamento)
    return agendamento

class TestProntuarioAPI:
    """Testes para os endpoints de Prontuário Eletrônico."""

    def test_get_or_create_prontuario(self, authenticated_client, paciente_teste):
        """Testa a obtenção ou criação de um prontuário para um paciente."""
        response = authenticated_client.get(f"/api/v1/prontuarios/paciente/{paciente_teste.paciente_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["paciente_id"] == str(paciente_teste.paciente_id)
        assert "id" in data

        # Tentar obter novamente, deve retornar o mesmo prontuário
        response2 = authenticated_client.get(f"/api/v1/prontuarios/paciente/{paciente_teste.paciente_id}")
        assert response2.status_code == 200
        assert response2.json()["id"] == data["id"]

    def test_create_evolucao(self, authenticated_client, paciente_teste, agendamento_teste):
        """Testa a criação de uma nova evolução no prontuário."""
        # Obter/Criar prontuário
        prontuario_response = authenticated_client.get(f"/api/v1/prontuarios/paciente/{paciente_teste.paciente_id}")
        prontuario_id = prontuario_response.json()["id"]

        evolucao_data = {
            "prontuario_id": prontuario_id,
            "profissional_id": authenticated_client.user_id,
            "agendamento_id": str(agendamento_teste.id),
            "descricao_clinica": "Paciente apresenta melhora significativa.",
            "dados_estruturados": {"pressao": "120/80", "temperatura": "36.5"}
        }
        response = authenticated_client.post("/api/v1/prontuarios/evolucoes", json=evolucao_data)
        assert response.status_code == 200
        data = response.json()
        assert data["prontuario_id"] == prontuario_id
        assert data["profissional_id"] == authenticated_client.user_id
        assert data["descricao_clinica"] == evolucao_data["descricao_clinica"]
        assert "id" in data

    def test_get_evolucoes_by_prontuario(self, authenticated_client, paciente_teste, agendamento_teste):
        """Testa a listagem de evoluções de um prontuário."""
        # Obter/Criar prontuário
        prontuario_response = authenticated_client.get(f"/api/v1/prontuarios/paciente/{paciente_teste.paciente_id}")
        prontuario_id = prontuario_response.json()["id"]

        # Criar algumas evoluções
        evolucao_data1 = {
            "prontuario_id": prontuario_id,
            "profissional_id": authenticated_client.user_id,
            "agendamento_id": str(agendamento_teste.id),
            "descricao_clinica": "Evolução 1"
        }
        authenticated_client.post("/api/v1/prontuarios/evolucoes", json=evolucao_data1)

        evolucao_data2 = {
            "prontuario_id": prontuario_id,
            "profissional_id": authenticated_client.user_id,
            "agendamento_id": str(agendamento_teste.id),
            "descricao_clinica": "Evolução 2"
        }
        authenticated_client.post("/api/v1/prontuarios/evolucoes", json=evolucao_data2)

        response = authenticated_client.get(f"/api/v1/prontuarios/{prontuario_id}/evolucoes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2 # Pode haver outras evoluções de outros testes
        assert any(e["descricao_clinica"] == "Evolução 1" for e in data)
        assert any(e["descricao_clinica"] == "Evolução 2" for e in data)

    def test_upload_anexo_evolucao(self, authenticated_client, paciente_teste, agendamento_teste):
        """Testa o upload de um anexo para uma evolução."""
        # Obter/Criar prontuário
        prontuario_response = authenticated_client.get(f"/api/v1/prontuarios/paciente/{paciente_teste.paciente_id}")
        prontuario_id = prontuario_response.json()["id"]

        # Criar uma evolução
        evolucao_data = {
            "prontuario_id": prontuario_id,
            "profissional_id": authenticated_client.user_id,
            "agendamento_id": str(agendamento_teste.id),
            "descricao_clinica": "Evolução com anexo"
        }
        evolucao_response = authenticated_client.post("/api/v1/prontuarios/evolucoes", json=evolucao_data)
        evolucao_id = evolucao_response.json()["id"]

        # Criar um arquivo de teste
        file_content = b"Conteúdo do arquivo de teste"
        files = {"file": ("teste.txt", file_content, "text/plain")}

        response = authenticated_client.post(
            f"/api/v1/prontuarios/evolucoes/{evolucao_id}/anexos",
            params={
                "tipo_anexo": TipoAnexo.OUTROS.value,
                "descricao": "Anexo de teste"
            },
            files=files
        )
        assert response.status_code == 200
        data = response.json()
        assert data["evolucao_id"] == evolucao_id
        assert data["tipo_anexo"] == TipoAnexo.OUTROS.value
        assert "caminho_arquivo" in data
        assert "id" in data
