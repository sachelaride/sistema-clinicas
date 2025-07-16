"""empty message

Revision ID: 0bc04ea374fb
Revises: 
Create Date: 2025-07-15 20:19:53.427002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.base import Base # Importar a Base do seu projeto

# revision identifiers, used by Alembic.
revision: str = '0bc04ea374fb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Cria todas as tabelas definidas na Base.metadata
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    # Remove todas as tabelas definidas na Base.metadata
    Base.metadata.drop_all(bind=op.get_bind())
