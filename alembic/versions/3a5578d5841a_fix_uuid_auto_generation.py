"""Fix UUID auto-generation

Revision ID: 3a5578d5841a
Revises: 6eab3fa7c508
Create Date: 2025-03-06 22:59:48.758936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a5578d5841a'
down_revision: Union[str, None] = '6eab3fa7c508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
