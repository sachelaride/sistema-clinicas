"""
Testes unitários para o módulo de estoque
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.base import Base
from database.session import get_db
from models.estoque import Produto, Fornecedor, LocalizacaoEstoque
from schemas.estoque import ProdutoCreate, FornecedorCreate, LocalizacaoEstoqueCreate

# Configurar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override da dependência do banco de dados para testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestProdutos:
    """Testes para endpoints de produtos"""
    
    def test_criar_produto(self):
        """Teste de criação de produto"""
        produto_data = {
            "nome": "Produto Teste",
            "descricao": "Descrição do produto teste",
            "unidade": "UN",
            "nivel_minimo_estoque": 10,
            "codigo_barras": "1234567890123"
        }
        
        response = client.post("/api/v1/estoque/produtos/", json=produto_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nome"] == produto_data["nome"]
        assert data["codigo_barras"] == produto_data["codigo_barras"]
        assert "produto_id" in data
    
    def test_listar_produtos(self):
        """Teste de listagem de produtos"""
        response = client.get("/api/v1/estoque/produtos/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_obter_produto(self):
        """Teste de obtenção de produto por ID"""
        # Primeiro criar um produto
        produto_data = {
            "nome": "Produto para Busca",
            "unidade": "UN",
            "nivel_minimo_estoque": 5
        }
        
        create_response = client.post("/api/v1/estoque/produtos/", json=produto_data)
        produto_id = create_response.json()["produto_id"]
        
        # Buscar o produto
        response = client.get(f"/api/v1/estoque/produtos/{produto_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["produto_id"] == produto_id
        assert data["nome"] == produto_data["nome"]
    
    def test_produto_nao_encontrado(self):
        """Teste de produto não encontrado"""
        response = client.get("/api/v1/estoque/produtos/99999")
        assert response.status_code == 404


class TestFornecedores:
    """Testes para endpoints de fornecedores"""
    
    def test_criar_fornecedor(self):
        """Teste de criação de fornecedor"""
        fornecedor_data = {
            "nome": "Fornecedor Teste",
            "cnpj": "12.345.678/0001-90",
            "contato_nome": "João Silva",
            "contato_email": "joao@fornecedor.com",
            "contato_telefone": "(11) 99999-9999"
        }
        
        response = client.post("/api/v1/estoque/fornecedores/", json=fornecedor_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nome"] == fornecedor_data["nome"]
        assert data["cnpj"] == fornecedor_data["cnpj"]
        assert "fornecedor_id" in data
    
    def test_listar_fornecedores(self):
        """Teste de listagem de fornecedores"""
        response = client.get("/api/v1/estoque/fornecedores/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestLocalizacoes:
    """Testes para endpoints de localizações"""
    
    def test_criar_localizacao(self):
        """Teste de criação de localização"""
        localizacao_data = {
            "nome": "Almoxarifado Central",
            "descricao": "Estoque principal da clínica",
            "clinica_id": 1
        }
        
        response = client.post("/api/v1/estoque/localizacoes/", json=localizacao_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nome"] == localizacao_data["nome"]
        assert "localizacao_id" in data


class TestMovimentosEstoque:
    """Testes para movimentos de estoque"""
    
    def setup_method(self):
        """Configurar dados para os testes"""
        # Criar produto
        produto_data = {
            "nome": "Produto para Movimento",
            "unidade": "UN",
            "nivel_minimo_estoque": 10
        }
        response = client.post("/api/v1/estoque/produtos/", json=produto_data)
        self.produto_id = response.json()["produto_id"]
        
        # Criar fornecedor
        fornecedor_data = {
            "nome": "Fornecedor para Movimento"
        }
        response = client.post("/api/v1/estoque/fornecedores/", json=fornecedor_data)
        self.fornecedor_id = response.json()["fornecedor_id"]
        
        # Criar localização
        localizacao_data = {
            "nome": "Local para Movimento"
        }
        response = client.post("/api/v1/estoque/localizacoes/", json=localizacao_data)
        self.localizacao_id = response.json()["localizacao_id"]
    
    def test_entrada_estoque(self):
        """Teste de entrada de estoque"""
        entrada_data = {
            "produto_id": self.produto_id,
            "quantidade": 100,
            "numero_lote": "LOTE001",
            "data_validade": (date.today() + timedelta(days=365)).isoformat(),
            "fornecedor_id": self.fornecedor_id,
            "localizacao_id": self.localizacao_id
        }
        
        response = client.post("/api/v1/estoque/movimentos/entrada/", params=entrada_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Entrada registrada com sucesso"
        assert "lote_id" in data
    
    def test_saida_estoque(self):
        """Teste de saída de estoque"""
        # Primeiro fazer uma entrada
        entrada_data = {
            "produto_id": self.produto_id,
            "quantidade": 50,
            "numero_lote": "LOTE002"
        }
        client.post("/api/v1/estoque/movimentos/entrada/", params=entrada_data)
        
        # Agora fazer a saída
        saida_data = {
            "produto_id": self.produto_id,
            "quantidade": 20,
            "referencia": "Consumo teste"
        }
        
        response = client.post("/api/v1/estoque/movimentos/saida/", params=saida_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Saída registrada com sucesso"
    
    def test_saida_estoque_insuficiente(self):
        """Teste de saída com estoque insuficiente"""
        saida_data = {
            "produto_id": self.produto_id,
            "quantidade": 1000,  # Quantidade maior que o estoque
            "referencia": "Teste estoque insuficiente"
        }
        
        response = client.post("/api/v1/estoque/movimentos/saida/", params=saida_data)
        assert response.status_code == 400


class TestRelatorios:
    """Testes para relatórios"""
    
    def test_estoque_consolidado(self):
        """Teste do relatório de estoque consolidado"""
        response = client.get("/api/v1/estoque/relatorios/estoque-consolidado/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_produtos_proximo_vencimento(self):
        """Teste de produtos próximos do vencimento"""
        response = client.get("/api/v1/estoque/lotes/proximo-vencimento/?dias=30")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__])

