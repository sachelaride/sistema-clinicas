"""
Operações CRUD para o módulo de usuários
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from models.usuario import (
    Usuario, Perfil, Permissao, PerfilAluno,
    LogAcesso, LogAuditoria
)
from models.clinica import Clinica
from schemas.usuario import (
    UsuarioCreate, UsuarioUpdate,
    PerfilCreate,
    PermissaoCreate,
    PerfilAlunoCreate, PerfilAlunoUpdate,
    UsuarioFiltro
)


# CRUD para Perfil
class CRUDPerfil:
    """Operações CRUD para perfis"""
    
    def get(self, db: Session, perfil_id: int) -> Optional[Perfil]:
        """Buscar perfil por ID"""
        return db.query(Perfil).filter(Perfil.perfil_id == perfil_id).first()
    
    def get_by_nome(self, db: Session, nome: str) -> Optional[Perfil]:
        """Buscar perfil por nome"""
        return db.query(Perfil).filter(Perfil.nome == nome).first()
    
    def get_multi(self, db: Session) -> List[Perfil]:
        """Listar todos os perfis"""
        return db.query(Perfil).all()
    
    def create(self, db: Session, obj_in: PerfilCreate) -> Perfil:
        """Criar novo perfil"""
        db_obj = Perfil(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def add_permissao(self, db: Session, perfil_id: int, permissao_id: int) -> bool:
        """Adicionar permissão ao perfil"""
        perfil = self.get(db, perfil_id)
        permissao = db.query(Permissao).filter(Permissao.permissao_id == permissao_id).first()
        
        if perfil and permissao and permissao not in perfil.permissoes:
            perfil.permissoes.append(permissao)
            db.commit()
            return True
        return False
    
    def remove_permissao(self, db: Session, perfil_id: int, permissao_id: int) -> bool:
        """Remover permissão do perfil"""
        perfil = self.get(db, perfil_id)
        permissao = db.query(Permissao).filter(Permissao.permissao_id == permissao_id).first()
        
        if perfil and permissao and permissao in perfil.permissoes:
            perfil.permissoes.remove(permissao)
            db.commit()
            return True
        return False


# CRUD para Permissao
class CRUDPermissao:
    """Operações CRUD para permissões"""
    
    def get(self, db: Session, permissao_id: int) -> Optional[Permissao]:
        """Buscar permissão por ID"""
        return db.query(Permissao).filter(Permissao.permissao_id == permissao_id).first()
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Permissao]:
        """Buscar permissão por código"""
        return db.query(Permissao).filter(Permissao.codigo == codigo).first()
    
    def get_multi(self, db: Session) -> List[Permissao]:
        """Listar todas as permissões"""
        return db.query(Permissao).all()
    
    def create(self, db: Session, obj_in: PermissaoCreate) -> Permissao:
        """Criar nova permissão"""
        db_obj = Permissao(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# CRUD para Usuario
class CRUDUsuario:
    """Operações CRUD para usuários"""
    
    def get(self, db: Session, usuario_id: UUID) -> Optional[Usuario]:
        """Buscar usuário por ID"""
        return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    
    def get_by_nome_usuario(self, db: Session, nome_usuario: str) -> Optional[Usuario]:
        """Buscar usuário por nome de usuário"""
        return db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        """Buscar usuário por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_rgm(self, db: Session, rgm: str) -> Optional[Usuario]:
        """Buscar usuário por RGM (aluno)"""
        return db.query(Usuario).join(PerfilAluno).filter(PerfilAluno.rgm == rgm).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Listar usuários com paginação"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    def search(self, db: Session, filtros: UsuarioFiltro, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Buscar usuários com filtros"""
        query = db.query(Usuario).options(joinedload(Usuario.clinica))
        
        if filtros.nome:
            query = query.filter(
                or_(
                    Usuario.nome_usuario.ilike(f"%{filtros.nome}%"),
                    Usuario.nome_completo.ilike(f"%{filtros.nome}%")
                )
            )
        
        if filtros.email:
            query = query.filter(Usuario.email.ilike(f"%{filtros.email}%"))
        
        if filtros.perfil_id:
            query = query.filter(Usuario.perfil_id == filtros.perfil_id)

        if filtros.clinica_id:
            query = query.filter(Usuario.clinica_id == filtros.clinica_id)
        
        if filtros.ativo is not None:
            query = query.filter(Usuario.ativo == filtros.ativo)
        
        if filtros.is_aluno is not None:
            if filtros.is_aluno:
                query = query.join(PerfilAluno)
            else:
                query = query.outerjoin(PerfilAluno).filter(PerfilAluno.usuario_id.is_(None))
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: UsuarioCreate) -> Usuario:
        """Criar novo usuário"""
        from core.security import get_password_hash
        
        # Validar se a clínica existe
        if obj_in.clinica_id and not db.query(Clinica).filter(Clinica.id == obj_in.clinica_id).first():
            raise ValueError("A clínica especificada não existe.")

        # Criar usuário
        usuario_data = obj_in.dict(exclude={'senha', 'perfil_aluno'})
        usuario_data['senha_hash'] = get_password_hash(obj_in.senha)
        db_usuario = Usuario(**usuario_data)
        
        db.add(db_usuario)
        db.flush()  # Para obter o ID do usuário
        
        # Criar perfil de aluno se fornecido
        if obj_in.perfil_aluno:
            perfil_aluno_data = obj_in.perfil_aluno.dict()
            perfil_aluno_data['usuario_id'] = db_usuario.usuario_id
            db_perfil_aluno = PerfilAluno(**perfil_aluno_data)
            db.add(db_perfil_aluno)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def update(self, db: Session, db_obj: Usuario, obj_in: UsuarioUpdate) -> Usuario:
        """Atualizar usuário"""
        update_data = obj_in.dict(exclude_unset=True)

        # Validar se a nova clínica existe
        if 'clinica_id' in update_data and update_data['clinica_id']:
            if not db.query(Clinica).filter(Clinica.id == update_data['clinica_id']).first():
                raise ValueError("A nova clínica especificada não existe.")

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_senha(self, db: Session, usuario_id: UUID, nova_senha: str) -> Optional[Usuario]:
        """Atualizar senha do usuário"""
        from core.security import get_password_hash
        
        usuario = self.get(db, usuario_id)
        if usuario:
            usuario.senha_hash = get_password_hash(nova_senha)
            db.commit()
            db.refresh(usuario)
        return usuario
    
    def activate(self, db: Session, usuario_id: UUID) -> Optional[Usuario]:
        """Ativar usuário"""
        usuario = self.get(db, usuario_id)
        if usuario:
            usuario.ativo = True
            db.commit()
            db.refresh(usuario)
        return usuario
    
    def deactivate(self, db: Session, usuario_id: UUID) -> Optional[Usuario]:
        """Desativar usuário"""
        usuario = self.get(db, usuario_id)
        if usuario:
            usuario.ativo = False
            db.commit()
            db.refresh(usuario)
        return usuario
    
    def get_alunos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Buscar apenas usuários que são alunos"""
        return db.query(Usuario).join(PerfilAluno).offset(skip).limit(limit).all()
    
    def get_permissoes_usuario(self, db: Session, usuario_id: UUID) -> List[str]:
        """Obter lista de códigos de permissões do usuário"""
        usuario = self.get(db, usuario_id)
        if usuario and usuario.perfil:
            return [p.codigo for p in usuario.perfil.permissoes]
        return []
    
    def has_permissao(self, db: Session, usuario_id: UUID, codigo_permissao: str) -> bool:
        """Verificar se usuário tem uma permissão específica"""
        permissoes = self.get_permissoes_usuario(db, usuario_id)
        return codigo_permissao in permissoes
    
    def get_estatisticas(self, db: Session) -> Dict[str, Any]:
        """Obter estatísticas de usuários"""
        total = db.query(Usuario).count()
        ativos = db.query(Usuario).filter(Usuario.ativo == True).count()
        
        # Usuários por perfil
        por_perfil = db.query(
            Perfil.nome,
            func.count(Usuario.usuario_id)
        ).join(Usuario).group_by(Perfil.nome).all()
        
        # Total de alunos
        total_alunos = db.query(Usuario).join(PerfilAluno).count()
        
        # Novos usuários no mês atual
        from datetime import date
        inicio_mes = date.today().replace(day=1)
        novos_mes = db.query(Usuario).filter(
            Usuario.criado_em >= inicio_mes
        ).count()
        
        return {
            "total_usuarios": total,
            "usuarios_ativos": ativos,
            "usuarios_por_perfil": {nome: count for nome, count in por_perfil},
            "total_alunos": total_alunos,
            "novos_usuarios_mes": novos_mes
        }


# CRUD para PerfilAluno
class CRUDPerfilAluno:
    """Operações CRUD para perfis de alunos"""
    
    def get(self, db: Session, usuario_id: UUID) -> Optional[PerfilAluno]:
        """Buscar perfil de aluno por ID do usuário"""
        return db.query(PerfilAluno).filter(PerfilAluno.usuario_id == usuario_id).first()
    
    def get_by_rgm(self, db: Session, rgm: str) -> Optional[PerfilAluno]:
        """Buscar perfil de aluno por RGM"""
        return db.query(PerfilAluno).filter(PerfilAluno.rgm == rgm).first()
    
    def create(self, db: Session, obj_in: PerfilAlunoCreate, usuario_id: UUID) -> PerfilAluno:
        """Criar novo perfil de aluno"""
        perfil_data = obj_in.dict()
        perfil_data['usuario_id'] = usuario_id
        db_obj = PerfilAluno(**perfil_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: PerfilAluno, obj_in: PerfilAlunoUpdate) -> PerfilAluno:
        """Atualizar perfil de aluno"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def incrementar_carga_horaria(self, db: Session, usuario_id: UUID, horas: int) -> Optional[PerfilAluno]:
        """Incrementar carga horária do aluno"""
        perfil = self.get(db, usuario_id)
        if perfil:
            perfil.carga_horaria_total += horas
            db.commit()
            db.refresh(perfil)
        return perfil


# CRUD para LogAcesso
class CRUDLogAcesso:
    """Operações CRUD para logs de acesso"""
    
    def create(self, db: Session, usuario_id: Optional[UUID], endereco_ip: str, 
               agente_usuario: str, sucesso: bool, motivo_falha: Optional[str] = None) -> LogAcesso:
        """Criar novo log de acesso"""
        db_obj = LogAcesso(
            usuario_id=usuario_id,
            endereco_ip=endereco_ip,
            agente_usuario=agente_usuario,
            sucesso=sucesso,
            motivo_falha=motivo_falha
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_usuario(self, db: Session, usuario_id: UUID, limit: int = 50) -> List[LogAcesso]:
        """Buscar logs de acesso por usuário"""
        return db.query(LogAcesso).filter(
            LogAcesso.usuario_id == usuario_id
        ).order_by(LogAcesso.horario_login.desc()).limit(limit).all()
    
    def get_tentativas_falha(self, db: Session, endereco_ip: str, minutos: int = 15) -> int:
        """Contar tentativas de login falhadas por IP nos últimos minutos"""
        from datetime import datetime, timedelta
        limite_tempo = datetime.now() - timedelta(minutes=minutos)
        
        return db.query(LogAcesso).filter(
            and_(
                LogAcesso.endereco_ip == endereco_ip,
                LogAcesso.sucesso == False,
                LogAcesso.horario_login >= limite_tempo
            )
        ).count()


# CRUD para LogAuditoria
class CRUDLogAuditoria:
    """Operações CRUD para logs de auditoria"""
    
    def create(self, db: Session, usuario_id: Optional[UUID], acao: str, 
               nome_tabela: Optional[str] = None, id_registro: Optional[str] = None,
               dados_antigos: Optional[str] = None, dados_novos: Optional[str] = None,
               endereco_ip: Optional[str] = None) -> LogAuditoria:
        """Criar novo log de auditoria"""
        db_obj = LogAuditoria(
            usuario_id=usuario_id,
            acao=acao,
            nome_tabela=nome_tabela,
            id_registro=id_registro,
            dados_antigos=dados_antigos,
            dados_novos=dados_novos,
            endereco_ip=endereco_ip
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_usuario(self, db: Session, usuario_id: UUID, limit: int = 100) -> List[LogAuditoria]:
        """Buscar logs de auditoria por usuário"""
        return db.query(LogAuditoria).filter(
            LogAuditoria.usuario_id == usuario_id
        ).order_by(LogAuditoria.horario_acao.desc()).limit(limit).all()
    
    def get_by_tabela(self, db: Session, nome_tabela: str, limit: int = 100) -> List[LogAuditoria]:
        """Buscar logs de auditoria por tabela"""
        return db.query(LogAuditoria).filter(
            LogAuditoria.nome_tabela == nome_tabela
        ).order_by(LogAuditoria.horario_acao.desc()).limit(limit).all()


# Instâncias dos CRUDs
crud_perfil = CRUDPerfil()
crud_permissao = CRUDPermissao()
crud_usuario = CRUDUsuario()
crud_perfil_aluno = CRUDPerfilAluno()
crud_log_acesso = CRUDLogAcesso()
crud_log_auditoria = CRUDLogAuditoria()

