"""Fix UserRole Enum to String

Revision ID: 518e0da76960
Revises: 3a5578d5841a
Create Date: 2025-03-06 23:11:48.231185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '518e0da76960'
down_revision: Union[str, None] = '3a5578d5841a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Convert 'role' column to String
    op.alter_column("users", "role", type_=sa.String(), existing_type=sa.Enum("student", "teacher", "admin", name="userrole"))

def downgrade():
    # Revert to Enum (only if you want to roll back)
    userrole_enum = sa.Enum("student", "teacher", "admin", name="userrole")
    op.alter_column("users", "role", type_=userrole_enum, existing_type=sa.String())