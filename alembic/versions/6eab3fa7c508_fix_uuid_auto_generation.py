"""Fix UUID auto-generation

Revision ID: 6eab3fa7c508
Revises: 49bcd7397177
Create Date: 2025-03-06 22:57:00.448379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6eab3fa7c508'
down_revision: Union[str, None] = '49bcd7397177'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_schools_id', table_name='schools')
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('STUDENT', 'TEACHER', 'ADMIN', name='user_role'),
               type_=sa.String(),
               existing_nullable=False)
    op.drop_index('ix_users_id', table_name='users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.alter_column('users', 'role',
               existing_type=sa.String(),
               type_=postgresql.ENUM('STUDENT', 'TEACHER', 'ADMIN', name='user_role'),
               existing_nullable=False)
    op.create_index('ix_schools_id', 'schools', ['id'], unique=False)
    # ### end Alembic commands ###
