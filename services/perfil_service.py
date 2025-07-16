"""
Serviços para o módulo de Perfis e Permissões.
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from crud.usuario import crud_perfil, crud_permissao, crud_usuario
from schemas.usuario import PerfilCreate, PermissaoCreate, UsuarioCreate
from core.security import get_password_hash

class PerfilService:
    def inicializar_permissoes_padrao(self, db: Session) -> List[Dict[str, str]]:
        """Inicializa as permissões padrão do sistema."""
        permissoes_base = [
            {"codigo": "admin:full", "descricao": "Acesso administrativo completo"},
            {"codigo": "paciente:create", "descricao": "Criar pacientes"},
            {"codigo": "paciente:read", "descricao": "Visualizar pacientes"},
            {"codigo": "paciente:update", "descricao": "Atualizar pacientes"},
            {"codigo": "paciente:delete", "descricao": "Excluir pacientes"},
            {"codigo": "usuario:create", "descricao": "Criar usuários"},
            {"codigo": "usuario:read", "descricao": "Visualizar usuários"},
            {"codigo": "usuario:update", "descricao": "Atualizar usuários"},
            {"codigo": "usuario:delete", "descricao": "Excluir usuários"},
            {"codigo": "estoque:create", "descricao": "Criar itens de estoque"},
            {"codigo": "estoque:read", "descricao": "Visualizar estoque"},
            {"codigo": "estoque:update", "descricao": "Atualizar estoque"},
            {"codigo": "estoque:delete", "descricao": "Excluir itens de estoque"},
            {"codigo": "agendamento:create", "descricao": "Criar agendamentos"},
            {"codigo": "agendamento:read", "descricao": "Visualizar agendamentos"},
            {"codigo": "agendamento:update", "descricao": "Atualizar agendamentos"},
            {"codigo": "agendamento:delete", "descricao": "Excluir agendamentos"},
            {"codigo": "prontuario:create", "descricao": "Criar prontuários/evoluções"},
            {"codigo": "prontuario:read", "descricao": "Visualizar prontuários"},
            {"codigo": "prontuario:update", "descricao": "Atualizar prontuários"},
            {"codigo": "prontuario:delete", "descricao": "Excluir prontuários"},
            {"codigo": "fila:create", "descricao": "Adicionar à fila"},
            {"codigo": "fila:read", "descricao": "Visualizar fila"},
            {"codigo": "fila:update", "descricao": "Atualizar status da fila"},
            {"codigo": "fila:call", "descricao": "Chamar paciente da fila"},
            {"codigo": "auditoria:read", "descricao": "Visualizar logs de auditoria"},
            {"codigo": "relatorio:read", "descricao": "Visualizar relatórios"},
            {"codigo": "relatorio:export", "descricao": "Exportar relatórios"},
        ]
        
        permissoes_criadas = []
        for p_data in permissoes_base:
            if not crud_permissao.get_by_codigo(db, p_data["codigo"]):
                permissao = crud_permissao.create(db, PermissaoCreate(**p_data))
                permissoes_criadas.append({"codigo": permissao.codigo, "id": permissao.permissao_id})
        return permissoes_criadas

    def inicializar_perfis_padrao(self, db: Session) -> List[Dict[str, Any]]:
        """Inicializa os perfis padrão do sistema e associa permissões."""
        perfis_config = {
            "Administrador": [
                "admin:full",
                "auditoria:read"
            ],
            "Recepcionista": [
                "paciente:create", "paciente:read", "paciente:update",
                "agendamento:create", "agendamento:read", "agendamento:update",
                "fila:create", "fila:read", "fila:call"
            ],
            "Profissional": [
                "paciente:read",
                "agendamento:read", "agendamento:update",
                "prontuario:create", "prontuario:read", "prontuario:update",
                "fila:read", "fila:call"
            ],
            "Aluno": [
                "paciente:read",
                "agendamento:read",
                "prontuario:read", "prontuario:create",
                "fila:read"
            ],
            "Coordenador": [
                "paciente:read", "paciente:update",
                "usuario:read",
                "estoque:read",
                "agendamento:read",
                "prontuario:read",
                "fila:read",
                "relatorio:read"
            ]
        }

        perfis_criados = []
        for perfil_nome, permissoes_codigos in perfis_config.items():
            perfil = crud_perfil.get_by_nome(db, perfil_nome)
            if not perfil:
                perfil = crud_perfil.create(db, PerfilCreate(nome=perfil_nome))
                perfis_criados.append({"nome": perfil.nome, "id": perfil.perfil_id})
            
            # Associar permissões
            for p_codigo in permissoes_codigos:
                permissao = crud_permissao.get_by_codigo(db, p_codigo)
                if permissao and permissao not in perfil.permissoes:
                    crud_perfil.add_permissao(db, perfil.perfil_id, permissao.permissao_id)
        
        # Criar usuário administrador padrão se não existir
        if not crud_usuario.get_by_nome_usuario(db, "admin"):
            admin_profile = crud_perfil.get_by_nome(db, "Administrador")
            if admin_profile:
                admin_user_data = UsuarioCreate(
                    nome_usuario="admin",
                    senha="adminpass", # Senha padrão, deve ser alterada!
                    nome_completo="Administrador do Sistema",
                    perfil_id=admin_profile.perfil_id,
                    email="admin@clinicas.com",
                    clinica_id=None # Administrador geral não associado a uma clínica específica
                )
                crud_usuario.create(db, admin_user_data)
                perfis_criados.append({"nome": "Usuário Admin Padrão", "usuario": "admin"})

        return perfis_criados

    def criar_perfil(self, db: Session, perfil_data: PerfilCreate):
        existing_perfil = crud_perfil.get_by_nome(db, perfil_data.nome)
        if existing_perfil:
            raise ValueError("Perfil com este nome já existe.")
        return crud_perfil.create(db, perfil_data)

    def criar_permissao(self, db: Session, permissao_data: PermissaoCreate):
        existing_permissao = crud_permissao.get_by_codigo(db, permissao_data.codigo)
        if existing_permissao:
            raise ValueError("Permissão com este código já existe.")
        return crud_permissao.create(db, permissao_data)

    def adicionar_permissao_perfil(self, db: Session, perfil_id: int, permissao_id: int, usuario_id: Any):
        perfil = crud_perfil.get(db, perfil_id)
        permissao = crud_permissao.get(db, permissao_id)
        if not perfil or not permissao:
            raise ValueError("Perfil ou Permissão não encontrados.")
        return crud_perfil.add_permissao(db, perfil_id, permissao_id)

    def remover_permissao_perfil(self, db: Session, perfil_id: int, permissao_id: int, usuario_id: Any):
        perfil = crud_perfil.get(db, perfil_id)
        permissao = crud_permissao.get(db, permissao_id)
        if not perfil or not permissao:
            raise ValueError("Perfil ou Permissão não encontrados.")
        return crud_perfil.remove_permissao(db, perfil_id, permissao_id)

perfil_service = PerfilService()
