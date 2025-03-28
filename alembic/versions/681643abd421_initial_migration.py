"""initial migration

Revision ID: 681643abd421
Revises: 
Create Date: 2025-03-27 04:33:34.161454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import uuid

# revision identifiers, used by Alembic.
revision: str = '681643abd421'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schools',
    sa.Column('id', sa.UUID(), default=uuid.uuid4, nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), default=uuid.uuid4, nullable=True),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('cellphone', sa.String(), nullable=True),
    sa.Column('school_id', sa.UUID(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cellphone')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('groups',
    sa.Column('id', sa.UUID(),default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('teacher_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_table('user_profile',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('group_students',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('group_id', sa.UUID(), nullable=True),
    sa.Column('student_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_students_id'), 'group_students', ['id'], unique=False)
    op.create_table('lessons',
    sa.Column('id', sa.UUID(), default=uuid.uuid4, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('group_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    op.drop_index(op.f('ix_group_students_id'), table_name='group_students')
    op.drop_table('group_students')
    op.drop_table('user_profile')
    op.drop_index(op.f('ix_groups_id'), table_name='groups')
    op.drop_table('groups')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('schools')
    # ### end Alembic commands ###
