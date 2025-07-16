"""
Configurações do Sistema de Clínicas

Este arquivo gerencia as configurações da aplicação, permitindo que valores
sejam carregados de variáveis de ambiente ou de um arquivo .env.

Para configurar o ambiente:
1. Crie um arquivo `.env` na raiz do projeto (ou em um caminho especificado).
2. Defina as variáveis de ambiente necessárias (ex: `DATABASE_URL="..."`).
3. Para produção, defina as variáveis diretamente no ambiente do servidor.

Exemplo de `.env`:
DATABASE_URL="postgresql://postgres:sua_senha_segura@127.0.0.1:5432/clinicas"
SECRET_KEY="uma_chave_secreta_muito_longa_e_aleatoria"
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=False
SMTP_HOST="smtp.seudominio.com"
SMTP_USER="seu_email@seudominio.com"
SMTP_PASSWORD="sua_senha_de_email"

"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações do banco de dados
    # DATABASE_URL deve ser fornecido via variável de ambiente ou .env
    # Ex: DATABASE_URL="postgresql://user:password@host:port/dbname"
    DATABASE_URL: str
    
    # Configurações de segurança
    # SECRET_KEY deve ser uma string longa e aleatória, gerada de forma segura.
    # Ex: SECRET_KEY="$(openssl rand -hex 32)"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações do servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False # Deve ser False em produção
    
    # Configurações de upload
    UPLOAD_DIR: str = "./uploads" # Caminho relativo ou absoluto
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Configurações de logs
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Configurações de email (para futuras implementações)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Configurações de backup
    BACKUP_DIR: str = "./backups"
    BACKUP_RETENTION_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra='ignore', env_file_encoding='utf-8')

# Instância global das configurações
settings = Settings()