"""Add subscriptions table

Revision ID: 003_subscriptions
Revises: 002_images
Create Date: 2024-01-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003_subscriptions'
down_revision: Union[str, None] = '002_images'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types for subscriptions (only if they don't exist)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE subscriptionplan AS ENUM ('weekly', 'monthly', 'yearly', 'free');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE subscriptionstatus AS ENUM ('active', 'canceled', 'expired', 'trial', 'past_due');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE billingprovider AS ENUM ('stripe', 'app_store', 'google_play', 'manual');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    
    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plan', postgresql.ENUM('weekly', 'monthly', 'yearly', 'free', name='subscriptionplan', create_type=False), nullable=False, server_default='free'),
        sa.Column('status', postgresql.ENUM('active', 'canceled', 'expired', 'trial', 'past_due', name='subscriptionstatus', create_type=False), nullable=False, server_default='active'),
        sa.Column('billing_provider', postgresql.ENUM('stripe', 'app_store', 'google_play', 'manual', name='billingprovider', create_type=False), nullable=True),
        sa.Column('provider_subscription_id', sa.String(), nullable=True),
        sa.Column('provider_customer_id', sa.String(), nullable=True),
        sa.Column('current_period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('canceled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trial_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ai_job_quota', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('ai_jobs_used', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('metadata', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=True)
    op.create_index(op.f('ix_subscriptions_provider_subscription_id'), 'subscriptions', ['provider_subscription_id'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_subscriptions_provider_subscription_id'), table_name='subscriptions')
    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')
    
    # Drop table
    op.drop_table('subscriptions')
    
    # Drop enum types
    op.execute("DROP TYPE billingprovider")
    op.execute("DROP TYPE subscriptionstatus")
    op.execute("DROP TYPE subscriptionplan")



