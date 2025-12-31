"""Add user role column

Revision ID: 005_user_role
Revises: 004_design_jobs
Create Date: 2024-01-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '005_user_role'
down_revision: Union[str, None] = '004_design_jobs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for user role
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin', 'super_admin')")
    
    # Add role column
    op.add_column('users', sa.Column('role', postgresql.ENUM('user', 'admin', 'super_admin', name='userrole', create_type=False), nullable=False, server_default='user'))
    
    # Create index on role
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)


def downgrade() -> None:
    # Drop index
    op.drop_index(op.f('ix_users_role'), table_name='users')
    
    # Drop column
    op.drop_column('users', 'role')
    
    # Drop enum type
    op.execute("DROP TYPE userrole")

