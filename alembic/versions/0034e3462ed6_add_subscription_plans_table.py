"""add_subscription_plans_table

Revision ID: 0034e3462ed6
Revises: 005_user_role
Create Date: 2026-01-01 11:05:02.175611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0034e3462ed6'
down_revision: Union[str, None] = '005_user_role'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create subscription_plans table
    op.create_table(
        'subscription_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(), nullable=False, server_default='USD'),
        sa.Column('ai_job_quota', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('period_days', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('features', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_plans_id'), 'subscription_plans', ['id'], unique=False)
    op.create_index(op.f('ix_subscription_plans_name'), 'subscription_plans', ['name'], unique=True)
    
    # Insert default plans
    op.execute("""
        INSERT INTO subscription_plans (name, display_name, description, price, currency, ai_job_quota, period_days, is_active, is_default, sort_order)
        VALUES
            ('free', 'Free Plan', 'Basic plan with limited features', 0, 'USD', 10, 30, true, true, 0),
            ('weekly', 'Weekly Plan', 'Weekly subscription plan', 9.99, 'USD', 100, 7, true, false, 1),
            ('monthly', 'Monthly Plan', 'Monthly subscription plan', 29.99, 'USD', 500, 30, true, false, 2),
            ('yearly', 'Yearly Plan', 'Yearly subscription plan', 299.99, 'USD', 6000, 365, true, false, 3)
    """)


def downgrade() -> None:
    # Drop subscription_plans table
    op.drop_index(op.f('ix_subscription_plans_name'), table_name='subscription_plans')
    op.drop_index(op.f('ix_subscription_plans_id'), table_name='subscription_plans')
    op.drop_table('subscription_plans')




