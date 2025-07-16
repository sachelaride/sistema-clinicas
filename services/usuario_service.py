"""
Serviço de usuários com lógica de negócios
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session

from crud.usuario import (
    crud_usuario, crud_perfil, crud_permissao, 
    crud_perfil_aluno, crud_log_auditoria
)
from schemas.usuario import (
    UsuarioCreate, UsuarioUpdate, UsuarioFiltro,
    PerfilCreate, PermissaoCreate,
    PerfilAlunoCreate, PerfilAlunoUpdate,
    EstatisticasUsuarios
)
from models.usuario import Usuario, Perfil
from core.security import SecurityUtils, get_password_hash


class UsuarioService:
    """Serviço de usuários com lógica de negócios"""
    
    def criar_usuario(self, db: Session, usuario_data: UsuarioCreate) -> Usuario:
        """Criar novo usuário com validações"""
        # Verificar se nome de usuário já existe
        existing = crud_usuario.get_by_nome_usuario(db, usuario_data.nome_usuario)
        if existing:
            raise ValueError("Nome de usuário já existe")
        
        # Verificar se email já existe (se fornecido)
        if usuario_data.email:
            existing = crud_usuario.get_by_email(db, usuario_data.email)
            if existing:
                raise ValueError("Email já está em uso")
        
        # Verificar se RGM já existe (se for aluno)
        if usuario_data.perfil_aluno:
            existing = crud_perfil_aluno.get_by_rgm(db, usuario_data.perfil_aluno.rgm)
            if existing:
                raise ValueError("RGM já está cadastrado")
        
        # Validar força da senha
        if not SecurityUtils.validate_password_strength(usuario_data.senha):
            raise ValueError("Senha deve ter pelo menos 6 caracteres, incluindo letras e números")
        
        return crud_usuario.create(db, usuario_data)
    
    def atualizar_usuario(self, db: Session, usuario_id: UUID, 
                         usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        """Atualizar usuário com validações"""
        usuario = crud_usuario.get(db, usuario_id)
        if not usuario:
            return None
        
        # Verificar email único se estiver sendo alterado
        if usuario_data.email and usuario_data.email != usuario.email:
            existing = crud_usuario.get_by_email(db, usuario_data.email)
            if existing and existing.usuario_id != usuario_id:
                raise ValueError("Email já está em uso")
        
        return crud_usuario.update(db, usuario, usuario_data)
    
    def buscar_usuarios(self, db: Session, filtros: UsuarioFiltro, 
                       skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Buscar usuários com filtros avançados"""
        return crud_usuario.search(db, filtros, skip, limit)
    
    def ativar_usuario(self, db: Session, usuario_id: UUID, admin_id: UUID) -> Optional[Usuario]:
        """Ativar usuário (admin)"""
        usuario = crud_usuario.activate(db, usuario_id)
        if usuario:
            # Registrar auditoria
            crud_log_auditoria.create(
                db=db,
                usuario_id=admin_id,
                acao="ACTIVATE_USER",
                nome_tabela="usuarios",
                id_registro=str(usuario_id)
            )
        return usuario
    
    def desativar_usuario(self, db: Session, usuario_id: UUID, admin_id: UUID) -> Optional[Usuario]:
        """Desativar usuário (admin)"""
        usuario = crud_usuario.deactivate(db, usuario_id)
        if usuario:
            # Registrar auditoria
            crud_log_auditoria.create(
                db=db,
                usuario_id=admin_id,
                acao="DEACTIVATE_USER",
                nome_tabela="usuarios",
                id_registro=str(usuario_id)
            )
        return usuario
    
    def resetar_senha(self, db: Session, usuario_id: UUID, admin_id: UUID) -> str:
        """Resetar senha do usuário (admin)"""
        usuario = crud_usuario.get(db, usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        # Gerar senha temporária
        nova_senha = SecurityUtils.generate_temp_password()
        
        # Atualizar senha
        crud_usuario.update_senha(db, usuario_id, nova_senha)
        
        # Registrar auditoria
        crud_log_auditoria.create(
            db=db,
            usuario_id=admin_id,
            acao="RESET_PASSWORD",
            nome_tabela="usuarios",
            id_registro=str(usuario_id)
        )
        
        return nova_senha
    
    def atualizar_perfil_aluno(self, db: Session, usuario_id: UUID, 
                              perfil_data: PerfilAlunoUpdate) -> Optional[Usuario]:
        """Atualizar perfil de aluno"""
        usuario = crud_usuario.get(db, usuario_id)
        if not usuario or not usuario.perfil_aluno:
            return None
        
        crud_perfil_aluno.update(db, usuario.perfil_aluno, perfil_data)
        db.refresh(usuario)
        return usuario
    
    def incrementar_carga_horaria(self, db: Session, usuario_id: UUID, horas: int) -> bool:
        """Incrementar carga horária do aluno"""
        perfil_aluno = crud_perfil_aluno.get(db, usuario_id)
        if not perfil_aluno:
            return False
        
        crud_perfil_aluno.incrementar_carga_horaria(db, usuario_id, horas)
        
        # Registrar auditoria
        crud_log_auditoria.create(
            db=db,
            usuario_id=usuario_id,
            acao="INCREMENT_HOURS",
            nome_tabela="perfis_alunos",
            id_registro=str(usuario_id),
            dados_novos=f"Incremento: {horas} horas"
        )
        
        return True
    
    def get_alunos_por_curso(self, db: Session, curso: str) -> List[Usuario]:
        """Obter alunos por curso"""
        from sqlalchemy import and_
        from models.usuario import PerfilAluno
        
        return db.query(Usuario).join(PerfilAluno).filter(
            PerfilAluno.curso.ilike(f"%{curso}%")
        ).all()
    
    def get_alunos_por_semestre(self, db: Session, semestre: int) -> List[Usuario]:
        """Obter alunos por semestre"""
        from models.usuario import PerfilAluno
        
        return db.query(Usuario).join(PerfilAluno).filter(
            PerfilAluno.semestre == semestre
        ).all()
    
    def get_ranking_carga_horaria(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Obter ranking de alunos por carga horária"""
        from sqlalchemy import desc
        from models.usuario import PerfilAluno
        
        resultados = db.query(
            Usuario.nome_completo,
            PerfilAluno.rgm,
            PerfilAluno.curso,
            PerfilAluno.carga_horaria_total
        ).join(PerfilAluno).order_by(
            desc(PerfilAluno.carga_horaria_total)
        ).limit(limit).all()
        
        return [
            {
                "nome": nome,
                "rgm": rgm,
                "curso": curso,
                "carga_horaria": carga_horaria
            }
            for nome, rgm, curso, carga_horaria in resultados
        ]
    
    def get_estatisticas(self, db: Session) -> EstatisticasUsuarios:
        """Obter estatísticas de usuários"""
        stats = crud_usuario.get_estatisticas(db)
        
        # Últimos logins por usuário (top 10)
        from crud.usuario import crud_log_acesso
        from sqlalchemy import desc, func
        from models.usuario import LogAcesso
        
        ultimos_logins = db.query(
            Usuario.nome_completo,
            func.max(LogAcesso.horario_login).label('ultimo_login')
        ).join(LogAcesso).filter(
            LogAcesso.sucesso == True
        ).group_by(Usuario.usuario_id, Usuario.nome_completo).order_by(
            desc('ultimo_login')
        ).limit(10).all()
        
        ultimo_login_dict = {
            nome: ultimo_login.isoformat() if ultimo_login else None
            for nome, ultimo_login in ultimos_logins
        }
        
        return EstatisticasUsuarios(
            total_usuarios=stats["total_usuarios"],
            usuarios_ativos=stats["usuarios_ativos"],
            usuarios_por_perfil=stats["usuarios_por_perfil"],
            total_alunos=stats["total_alunos"],
            novos_usuarios_mes=stats["novos_usuarios_mes"],
            ultimo_login_usuarios=ultimo_login_dict
        )


class PerfilService:
    """Serviço de perfis e permissões"""
    
    def criar_perfil(self, db: Session, perfil_data: PerfilCreate) -> Perfil:
        """Criar novo perfil"""
        # Verificar se nome já existe
        existing = crud_perfil.get_by_nome(db, perfil_data.nome)
        if existing:
            raise ValueError("Nome do perfil já existe")
        
        return crud_perfil.create(db, perfil_data)
    
    def adicionar_permissao_perfil(self, db: Session, perfil_id: int, 
                                  permissao_id: int, admin_id: UUID) -> bool:
        """Adicionar permissão ao perfil"""
        sucesso = crud_perfil.add_permissao(db, perfil_id, permissao_id)
        
        if sucesso:
            # Registrar auditoria
            crud_log_auditoria.create(
                db=db,
                usuario_id=admin_id,
                acao="ADD_PERMISSION",
                nome_tabela="perfil_permissoes",
                dados_novos=f"Perfil {perfil_id} + Permissão {permissao_id}"
            )
        
        return sucesso
    
    def remover_permissao_perfil(self, db: Session, perfil_id: int, 
                                permissao_id: int, admin_id: UUID) -> bool:
        """Remover permissão do perfil"""
        sucesso = crud_perfil.remove_permissao(db, perfil_id, permissao_id)
        
        if sucesso:
            # Registrar auditoria
            crud_log_auditoria.create(
                db=db,
                usuario_id=admin_id,
                acao="REMOVE_PERMISSION",
                nome_tabela="perfil_permissoes",
                dados_antigos=f"Perfil {perfil_id} + Permissão {permissao_id}"
            )
        
        return sucesso
    
    def criar_permissao(self, db: Session, permissao_data: PermissaoCreate):
        """Criar nova permissão"""
        # Verificar se código já existe
        existing = crud_permissao.get_by_codigo(db, permissao_data.codigo)
        if existing:
            raise ValueError("Código da permissão já existe")
        
        return crud_permissao.create(db, permissao_data)
    
    def inicializar_perfis_padrao(self, db: Session) -> Dict[str, int]:
        """Inicializar perfis padrão do sistema"""
        perfis_padrao = [
            {"nome": "Administrador", "permissoes": ["admin:full"]},
            {"nome": "Coordenador", "permissoes": ["paciente:read", "paciente:update", "usuario:read", "relatorio:read"]},
            {"nome": "Aluno", "permissoes": ["paciente:read", "estoque:read"]},
            {"nome": "Recepcionista", "permissões": ["paciente:create", "paciente:read", "paciente:update"]},
        ]
        
        perfis_criados = {}
        
        for perfil_info in perfis_padrao:
            # Verificar se perfil já existe
            existing = crud_perfil.get_by_nome(db, perfil_info["nome"])
            if not existing:
                perfil_data = PerfilCreate(nome=perfil_info["nome"])
                perfil = crud_perfil.create(db, perfil_data)
                perfis_criados[perfil.nome] = perfil.perfil_id
            else:
                perfis_criados[existing.nome] = existing.perfil_id
        
        return perfis_criados
    
    def inicializar_permissoes_padrao(self, db: Session) -> List[int]:
        """Inicializar permissões padrão do sistema"""
        from core.security import Permissions
        
        permissoes_padrao = [
            {"codigo": Permissions.PACIENTE_CREATE, "descricao": "Criar pacientes"},
            {"codigo": Permissions.PACIENTE_READ, "descricao": "Visualizar pacientes"},
            {"codigo": Permissions.PACIENTE_UPDATE, "descricao": "Atualizar pacientes"},
            {"codigo": Permissions.PACIENTE_DELETE, "descricao": "Excluir pacientes"},
            {"codigo": Permissions.USUARIO_CREATE, "descricao": "Criar usuários"},
            {"codigo": Permissions.USUARIO_READ, "descricao": "Visualizar usuários"},
            {"codigo": Permissions.USUARIO_UPDATE, "descricao": "Atualizar usuários"},
            {"codigo": Permissions.USUARIO_DELETE, "descricao": "Excluir usuários"},
            {"codigo": Permissions.ESTOQUE_CREATE, "descricao": "Criar itens de estoque"},
            {"codigo": Permissions.ESTOQUE_READ, "descricao": "Visualizar estoque"},
            {"codigo": Permissions.ESTOQUE_UPDATE, "descricao": "Atualizar estoque"},
            {"codigo": Permissions.ESTOQUE_DELETE, "descricao": "Excluir itens de estoque"},
            {"codigo": Permissions.RELATORIO_READ, "descricao": "Visualizar relatórios"},
            {"codigo": Permissions.RELATORIO_EXPORT, "descricao": "Exportar relatórios"},
            {"codigo": Permissions.ADMIN_FULL, "descricao": "Acesso administrativo completo"},
            {"codigo": Permissions.LOG_READ, "descricao": "Visualizar logs"},
            {"codigo": Permissions.AUDITORIA_READ, "descricao": "Visualizar auditoria"},
        ]
        
        permissoes_criadas = []
        
        for perm_info in permissoes_padrao:
            # Verificar se permissão já existe
            existing = crud_permissao.get_by_codigo(db, perm_info["codigo"])
            if not existing:
                perm_data = PermissaoCreate(**perm_info)
                permissao = crud_permissao.create(db, perm_data)
                permissoes_criadas.append(permissao.permissao_id)
            else:
                permissoes_criadas.append(existing.permissao_id)
        
        return permissoes_criadas


# Instâncias dos serviços
usuario_service = UsuarioService()
perfil_service = PerfilService()

