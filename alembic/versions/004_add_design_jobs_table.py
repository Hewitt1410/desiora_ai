"""Add design_jobs table

Revision ID: 004_design_jobs
Revises: 003_subscriptions
Create Date: 2024-01-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '004_design_jobs'
down_revision: Union[str, None] = '003_subscriptions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for job status
    op.execute("CREATE TYPE jobstatus AS ENUM ('pending', 'processing', 'completed', 'failed', 'retrying')")
    
    # Create design_jobs table
    op.create_table(
        'design_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('job_type', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'processing', 'completed', 'failed', 'retrying', name='jobstatus', create_type=False), nullable=False, server_default='pending'),
        sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('result_urls', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('result_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('processing_time_seconds', sa.Integer(), nullable=True),
        sa.Column('queue_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_design_jobs_id'), 'design_jobs', ['id'], unique=False)
    op.create_index(op.f('ix_design_jobs_user_id'), 'design_jobs', ['user_id'], unique=False)
    op.create_index(op.f('ix_design_jobs_status'), 'design_jobs', ['status'], unique=False)
    op.create_index(op.f('ix_design_jobs_queue_id'), 'design_jobs', ['queue_id'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_design_jobs_queue_id'), table_name='design_jobs')
    op.drop_index(op.f('ix_design_jobs_status'), table_name='design_jobs')
    op.drop_index(op.f('ix_design_jobs_user_id'), table_name='design_jobs')
    op.drop_index(op.f('ix_design_jobs_id'), table_name='design_jobs')
    
    # Drop table
    op.drop_table('design_jobs')
    
    # Drop enum type
    op.execute("DROP TYPE jobstatus")

