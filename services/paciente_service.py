"""
Serviço de pacientes com lógica de negócios
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import UploadFile
import json

from crud.paciente import (
    crud_paciente, crud_responsavel_legal, crud_tipo_documento,
    crud_documento_paciente, crud_consentimento_paciente
)
from schemas.paciente import (
    PacienteCreate, PacienteUpdate, PacienteFiltro,
    ResponsavelLegalCreate,
    DocumentoPacienteCreate,
    ConsentimentoPacienteCreate,
    EstatisticasPacientes
)
from models.paciente import Paciente


class PacienteService:
    """Serviço de pacientes com lógica de negócios"""
    
    def __init__(self):
        self.upload_path = "/uploads/documentos/"
    
    def criar_paciente(self, db: Session, paciente_data: PacienteCreate) -> Paciente:
        """Criar novo paciente com validações"""
        # Verificar se já existe paciente com mesmo email
        if paciente_data.email:
            existing = crud_paciente.get_by_email(db, paciente_data.email)
            if existing:
                raise ValueError("Já existe um paciente com este email")
        
        # Verificar se já existe paciente com mesmo telefone
        if paciente_data.telefone:
            existing = crud_paciente.get_by_telefone(db, paciente_data.telefone)
            if existing:
                raise ValueError("Já existe um paciente com este telefone")
        
        # Criar paciente
        paciente = crud_paciente.create(db, paciente_data)
        
        # Criar consentimento básico LGPD
        consentimento_lgpd = ConsentimentoPacienteCreate(
            paciente_id=paciente.paciente_id,
            tipo_consentimento="LGPD_BASICO",
            detalhes="Consentimento para tratamento de dados pessoais conforme LGPD"
        )
        crud_consentimento_paciente.create(db, consentimento_lgpd)
        
        return paciente
    
    def atualizar_paciente(self, db: Session, paciente_id: UUID, 
                          paciente_data: PacienteUpdate) -> Optional[Paciente]:
        """Atualizar paciente com validações"""
        paciente = crud_paciente.get(db, paciente_id)
        if not paciente:
            return None
        
        # Verificar email único se estiver sendo alterado
        if paciente_data.email and paciente_data.email != paciente.email:
            existing = crud_paciente.get_by_email(db, paciente_data.email)
            if existing and existing.paciente_id != paciente_id:
                raise ValueError("Já existe um paciente com este email")
        
        # Verificar telefone único se estiver sendo alterado
        if paciente_data.telefone and paciente_data.telefone != paciente.telefone:
            existing = crud_paciente.get_by_telefone(db, paciente_data.telefone)
            if existing and existing.paciente_id != paciente_id:
                raise ValueError("Já existe um paciente com este telefone")
        
        return crud_paciente.update(db, paciente, paciente_data)
    
    def buscar_pacientes(self, db: Session, filtros: PacienteFiltro, 
                        skip: int = 0, limit: int = 100) -> List[Paciente]:
        """Buscar pacientes com filtros avançados"""
        return crud_paciente.search(db, filtros, skip, limit)
    
    def adicionar_responsavel(self, db: Session, responsavel_data: ResponsavelLegalCreate):
        """Adicionar responsável legal ao paciente"""
        # Verificar se paciente existe
        paciente = crud_paciente.get(db, responsavel_data.paciente_id)
        if not paciente:
            raise ValueError("Paciente não encontrado")
        
        # Verificar se CPF já está cadastrado (se fornecido)
        if responsavel_data.cpf:
            existing = crud_responsavel_legal.get_by_cpf(db, responsavel_data.cpf)
            if existing:
                raise ValueError("Já existe um responsável com este CPF")
        
        return crud_responsavel_legal.create(db, responsavel_data)
    
    def upload_documento(self, db: Session, paciente_id: UUID, 
                        tipo_id: Optional[int], arquivo: UploadFile) -> Dict[str, Any]:
        """Upload de documento do paciente"""
        import os
        import uuid
        
        # Verificar se paciente existe
        paciente = crud_paciente.get(db, paciente_id)
        if not paciente:
            raise ValueError("Paciente não encontrado")
        
        # Gerar nome único para o arquivo
        file_extension = arquivo.filename.split('.')[-1] if '.' in arquivo.filename else ''
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.upload_path, str(paciente_id), unique_filename)
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            content = arquivo.file.read()
            buffer.write(content)
        
        # Simular OCR (em produção, integrar com serviço real)
        dados_ocr = self._simular_ocr(arquivo.filename, content)
        
        # Criar registro no banco
        documento_data = DocumentoPacienteCreate(
            paciente_id=paciente_id,
            tipo_id=tipo_id,
            dados_ocr=dados_ocr,
            caminho_arquivo=file_path
        )
        
        documento = crud_documento_paciente.create(db, documento_data)
        
        return {
            "documento_id": documento.documento_id,
            "caminho_arquivo": file_path,
            "dados_ocr": dados_ocr,
            "tamanho_arquivo": len(content)
        }
    
    def registrar_consentimento(self, db: Session, consentimento_data: ConsentimentoPacienteCreate):
        """Registrar consentimento LGPD"""
        # Verificar se paciente existe
        paciente = crud_paciente.get(db, consentimento_data.paciente_id)
        if not paciente:
            raise ValueError("Paciente não encontrado")
        
        # Verificar se já existe consentimento do mesmo tipo
        existing = crud_consentimento_paciente.get_by_tipo(
            db, consentimento_data.paciente_id, consentimento_data.tipo_consentimento
        )
        
        if existing and existing.ativo:
            # Revogar consentimento anterior
            crud_consentimento_paciente.revogar_consentimento(db, existing.consentimento_id)
        
        return crud_consentimento_paciente.create(db, consentimento_data)
    
    def get_aniversariantes_mes(self, db: Session, mes: Optional[int] = None) -> List[Paciente]:
        """Obter aniversariantes do mês"""
        if mes is None:
            mes = date.today().month
        return crud_paciente.get_aniversariantes_mes(db, mes)
    
    def get_pacientes_por_idade(self, db: Session, idade_min: int, idade_max: int) -> List[Paciente]:
        """Obter pacientes por faixa etária"""
        return crud_paciente.get_por_faixa_etaria(db, idade_min, idade_max)
    
    def get_estatisticas(self, db: Session) -> EstatisticasPacientes:
        """Obter estatísticas de pacientes"""
        stats = crud_paciente.get_estatisticas(db)
        
        # Calcular faixas etárias
        faixas_etarias = {
            "0-17": len(crud_paciente.get_por_faixa_etaria(db, 0, 17)),
            "18-29": len(crud_paciente.get_por_faixa_etaria(db, 18, 29)),
            "30-49": len(crud_paciente.get_por_faixa_etaria(db, 30, 49)),
            "50-64": len(crud_paciente.get_por_faixa_etaria(db, 50, 64)),
            "65+": len(crud_paciente.get_por_faixa_etaria(db, 65, 120))
        }
        
        return EstatisticasPacientes(
            total_pacientes=stats["total_pacientes"],
            pacientes_por_sexo=stats["pacientes_por_sexo"],
            pacientes_por_faixa_etaria=faixas_etarias,
            novos_pacientes_mes=stats["novos_pacientes_mes"],
            pacientes_com_responsavel=stats["pacientes_com_responsavel"],
            pacientes_com_documentos=stats["pacientes_com_documentos"]
        )
    
    def validar_documentos_obrigatorios(self, db: Session, paciente_id: UUID) -> Dict[str, Any]:
        """Validar se paciente possui todos os documentos obrigatórios"""
        # Obter tipos de documentos obrigatórios
        tipos_obrigatorios = crud_tipo_documento.get_obrigatorios(db)
        
        # Obter documentos do paciente
        documentos_paciente = crud_documento_paciente.get_by_paciente(db, paciente_id)
        tipos_paciente = {doc.tipo_id for doc in documentos_paciente if doc.tipo_id}
        
        # Verificar quais estão faltando
        faltando = []
        for tipo in tipos_obrigatorios:
            if tipo.tipo_id not in tipos_paciente:
                faltando.append({
                    "tipo_id": tipo.tipo_id,
                    "nome": tipo.nome,
                    "descricao": tipo.descricao
                })
        
        return {
            "completo": len(faltando) == 0,
            "documentos_faltando": faltando,
            "total_obrigatorios": len(tipos_obrigatorios),
            "total_enviados": len([t for t in tipos_obrigatorios if t.tipo_id in tipos_paciente])
        }
    
    def atualizar_perfil_epidemiologico(self, db: Session, paciente_id: UUID, 
                                       dados: Dict[str, Any]) -> Optional[Paciente]:
        """Atualizar perfil epidemiológico do paciente"""
        paciente = crud_paciente.get(db, paciente_id)
        if not paciente:
            return None
        
        # Mesclar com dados existentes
        perfil_atual = paciente.perfil_epidemiologico or {}
        perfil_atual.update(dados)
        
        # Adicionar timestamp da atualização
        perfil_atual["ultima_atualizacao"] = datetime.now().isoformat()
        
        # Atualizar paciente
        paciente_update = PacienteUpdate(perfil_epidemiologico=perfil_atual)
        return crud_paciente.update(db, paciente, paciente_update)
    
    def _simular_ocr(self, filename: str, content: bytes) -> Optional[str]:
        """Simular extração OCR de documentos"""
        # Em produção, integrar com serviço real de OCR
        # Por enquanto, retornar dados simulados baseados no tipo de arquivo
        
        if not filename:
            return None
        
        filename_lower = filename.lower()
        
        if 'rg' in filename_lower:
            return json.dumps({
                "tipo_documento": "RG",
                "numero": "12.345.678-9",
                "orgao_expedidor": "SSP/SP",
                "data_expedicao": "2020-01-15",
                "extraido_em": datetime.now().isoformat()
            })
        elif 'cpf' in filename_lower:
            return json.dumps({
                "tipo_documento": "CPF",
                "numero": "123.456.789-00",
                "situacao": "Regular",
                "extraido_em": datetime.now().isoformat()
            })
        elif 'comprovante' in filename_lower:
            return json.dumps({
                "tipo_documento": "Comprovante de Residência",
                "endereco": "Rua das Flores, 123",
                "cep": "01234-567",
                "cidade": "São Paulo",
                "extraido_em": datetime.now().isoformat()
            })
        
        return json.dumps({
            "tipo_documento": "Documento Genérico",
            "arquivo_original": filename,
            "tamanho_bytes": len(content),
            "extraido_em": datetime.now().isoformat()
        })


# Instância do serviço
paciente_service = PacienteService()

