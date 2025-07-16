"""
Operações CRUD para o módulo de pacientes
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract

from models.paciente import (
    Paciente, ResponsavelLegal, TipoDocumento, 
    DocumentoPaciente, ConsentimentoPaciente
)
from schemas.paciente import (
    PacienteCreate, PacienteUpdate,
    ResponsavelLegalCreate,
    TipoDocumentoCreate,
    DocumentoPacienteCreate,
    ConsentimentoPacienteCreate,
    PacienteFiltro
)


# CRUD para Paciente
class CRUDPaciente:
    """Operações CRUD para pacientes"""
    
    def get(self, db: Session, paciente_id: UUID) -> Optional[Paciente]:
        """Buscar paciente por ID"""
        return db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Paciente]:
        """Buscar paciente por email"""
        return db.query(Paciente).filter(Paciente.email == email).first()
    
    def get_by_telefone(self, db: Session, telefone: str) -> Optional[Paciente]:
        """Buscar paciente por telefone"""
        return db.query(Paciente).filter(Paciente.telefone == telefone).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
        """Listar pacientes com paginação"""
        return db.query(Paciente).offset(skip).limit(limit).all()
    
    def search(self, db: Session, filtros: PacienteFiltro, skip: int = 0, limit: int = 100) -> List[Paciente]:
        """Buscar pacientes com filtros"""
        query = db.query(Paciente)
        
        if filtros.nome:
            query = query.filter(
                or_(
                    Paciente.nome.ilike(f"%{filtros.nome}%"),
                    Paciente.sobrenome.ilike(f"%{filtros.nome}%")
                )
            )
        
        if filtros.email:
            query = query.filter(Paciente.email.ilike(f"%{filtros.email}%"))
        
        if filtros.telefone:
            query = query.filter(Paciente.telefone.ilike(f"%{filtros.telefone}%"))
        
        if filtros.sexo:
            query = query.filter(Paciente.sexo == filtros.sexo)
        
        if filtros.data_nascimento_inicio:
            query = query.filter(Paciente.data_nascimento >= filtros.data_nascimento_inicio)
        
        if filtros.data_nascimento_fim:
            query = query.filter(Paciente.data_nascimento <= filtros.data_nascimento_fim)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: PacienteCreate) -> Paciente:
        """Criar novo paciente"""
        db_obj = Paciente(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: Paciente, obj_in: PacienteUpdate) -> Paciente:
        """Atualizar paciente"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, paciente_id: UUID) -> Optional[Paciente]:
        """Excluir paciente"""
        obj = db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def get_aniversariantes_mes(self, db: Session, mes: int) -> List[Paciente]:
        """Buscar aniversariantes do mês"""
        return db.query(Paciente).filter(
            extract('month', Paciente.data_nascimento) == mes
        ).all()
    
    def get_por_faixa_etaria(self, db: Session, idade_min: int, idade_max: int) -> List[Paciente]:
        """Buscar pacientes por faixa etária"""
        data_max = date.today().replace(year=date.today().year - idade_min)
        data_min = date.today().replace(year=date.today().year - idade_max - 1)
        
        return db.query(Paciente).filter(
            and_(
                Paciente.data_nascimento >= data_min,
                Paciente.data_nascimento <= data_max
            )
        ).all()
    
    def get_estatisticas(self, db: Session) -> Dict[str, Any]:
        """Obter estatísticas de pacientes"""
        total = db.query(Paciente).count()
        
        # Pacientes por sexo
        por_sexo = db.query(
            Paciente.sexo,
            func.count(Paciente.paciente_id)
        ).group_by(Paciente.sexo).all()
        
        # Novos pacientes no mês atual
        inicio_mes = date.today().replace(day=1)
        novos_mes = db.query(Paciente).filter(
            Paciente.criado_em >= inicio_mes
        ).count()
        
        # Pacientes com responsável
        com_responsavel = db.query(Paciente).join(ResponsavelLegal).count()
        
        # Pacientes com documentos
        com_documentos = db.query(Paciente).join(DocumentoPaciente).count()
        
        return {
            "total_pacientes": total,
            "pacientes_por_sexo": {sexo: count for sexo, count in por_sexo},
            "novos_pacientes_mes": novos_mes,
            "pacientes_com_responsavel": com_responsavel,
            "pacientes_com_documentos": com_documentos
        }


# CRUD para ResponsavelLegal
class CRUDResponsavelLegal:
    """Operações CRUD para responsáveis legais"""
    
    def get(self, db: Session, responsavel_id: UUID) -> Optional[ResponsavelLegal]:
        """Buscar responsável por ID"""
        return db.query(ResponsavelLegal).filter(
            ResponsavelLegal.responsavel_id == responsavel_id
        ).first()
    
    def get_by_paciente(self, db: Session, paciente_id: UUID) -> List[ResponsavelLegal]:
        """Buscar responsáveis por paciente"""
        return db.query(ResponsavelLegal).filter(
            ResponsavelLegal.paciente_id == paciente_id
        ).all()
    
    def get_by_cpf(self, db: Session, cpf: str) -> Optional[ResponsavelLegal]:
        """Buscar responsável por CPF"""
        return db.query(ResponsavelLegal).filter(ResponsavelLegal.cpf == cpf).first()
    
    def create(self, db: Session, obj_in: ResponsavelLegalCreate) -> ResponsavelLegal:
        """Criar novo responsável legal"""
        db_obj = ResponsavelLegal(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, responsavel_id: UUID) -> Optional[ResponsavelLegal]:
        """Excluir responsável legal"""
        obj = db.query(ResponsavelLegal).filter(
            ResponsavelLegal.responsavel_id == responsavel_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# CRUD para TipoDocumento
class CRUDTipoDocumento:
    """Operações CRUD para tipos de documentos"""
    
    def get(self, db: Session, tipo_id: int) -> Optional[TipoDocumento]:
        """Buscar tipo de documento por ID"""
        return db.query(TipoDocumento).filter(TipoDocumento.tipo_id == tipo_id).first()
    
    def get_by_nome(self, db: Session, nome: str) -> Optional[TipoDocumento]:
        """Buscar tipo de documento por nome"""
        return db.query(TipoDocumento).filter(TipoDocumento.nome == nome).first()
    
    def get_multi(self, db: Session) -> List[TipoDocumento]:
        """Listar todos os tipos de documentos"""
        return db.query(TipoDocumento).all()
    
    def get_obrigatorios(self, db: Session) -> List[TipoDocumento]:
        """Buscar tipos de documentos obrigatórios"""
        return db.query(TipoDocumento).filter(TipoDocumento.obrigatorio == True).all()
    
    def create(self, db: Session, obj_in: TipoDocumentoCreate) -> TipoDocumento:
        """Criar novo tipo de documento"""
        db_obj = TipoDocumento(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# CRUD para DocumentoPaciente
class CRUDDocumentoPaciente:
    """Operações CRUD para documentos de pacientes"""
    
    def get(self, db: Session, documento_id: UUID) -> Optional[DocumentoPaciente]:
        """Buscar documento por ID"""
        return db.query(DocumentoPaciente).filter(
            DocumentoPaciente.documento_id == documento_id
        ).first()
    
    def get_by_paciente(self, db: Session, paciente_id: UUID) -> List[DocumentoPaciente]:
        """Buscar documentos por paciente"""
        return db.query(DocumentoPaciente).filter(
            DocumentoPaciente.paciente_id == paciente_id
        ).all()
    
    def get_by_tipo(self, db: Session, paciente_id: UUID, tipo_id: int) -> Optional[DocumentoPaciente]:
        """Buscar documento específico por tipo e paciente"""
        return db.query(DocumentoPaciente).filter(
            and_(
                DocumentoPaciente.paciente_id == paciente_id,
                DocumentoPaciente.tipo_id == tipo_id
            )
        ).first()
    
    def create(self, db: Session, obj_in: DocumentoPacienteCreate) -> DocumentoPaciente:
        """Criar novo documento"""
        db_obj = DocumentoPaciente(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, documento_id: UUID) -> Optional[DocumentoPaciente]:
        """Excluir documento"""
        obj = db.query(DocumentoPaciente).filter(
            DocumentoPaciente.documento_id == documento_id
        ).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# CRUD para ConsentimentoPaciente
class CRUDConsentimentoPaciente:
    """Operações CRUD para consentimentos de pacientes"""
    
    def get(self, db: Session, consentimento_id: int) -> Optional[ConsentimentoPaciente]:
        """Buscar consentimento por ID"""
        return db.query(ConsentimentoPaciente).filter(
            ConsentimentoPaciente.consentimento_id == consentimento_id
        ).first()
    
    def get_by_paciente(self, db: Session, paciente_id: UUID) -> List[ConsentimentoPaciente]:
        """Buscar consentimentos por paciente"""
        return db.query(ConsentimentoPaciente).filter(
            ConsentimentoPaciente.paciente_id == paciente_id
        ).all()
    
    def get_ativos_by_paciente(self, db: Session, paciente_id: UUID) -> List[ConsentimentoPaciente]:
        """Buscar consentimentos ativos por paciente"""
        return db.query(ConsentimentoPaciente).filter(
            and_(
                ConsentimentoPaciente.paciente_id == paciente_id,
                ConsentimentoPaciente.ativo == True
            )
        ).all()
    
    def get_by_tipo(self, db: Session, paciente_id: UUID, tipo: str) -> Optional[ConsentimentoPaciente]:
        """Buscar consentimento por tipo e paciente"""
        return db.query(ConsentimentoPaciente).filter(
            and_(
                ConsentimentoPaciente.paciente_id == paciente_id,
                ConsentimentoPaciente.tipo_consentimento == tipo
            )
        ).first()
    
    def create(self, db: Session, obj_in: ConsentimentoPacienteCreate) -> ConsentimentoPaciente:
        """Criar novo consentimento"""
        db_obj = ConsentimentoPaciente(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def revogar_consentimento(self, db: Session, consentimento_id: int) -> Optional[ConsentimentoPaciente]:
        """Revogar consentimento (marcar como inativo)"""
        obj = self.get(db, consentimento_id)
        if obj:
            obj.ativo = False
            db.commit()
            db.refresh(obj)
        return obj


# Instâncias dos CRUDs
crud_paciente = CRUDPaciente()
crud_responsavel_legal = CRUDResponsavelLegal()
crud_tipo_documento = CRUDTipoDocumento()
crud_documento_paciente = CRUDDocumentoPaciente()
crud_consentimento_paciente = CRUDConsentimentoPaciente()

