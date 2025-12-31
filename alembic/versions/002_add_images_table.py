"""Add images table

Revision ID: 002_images
Revises: 001_initial
Create Date: 2024-01-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_images'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types for images
    op.execute("CREATE TYPE imagetype AS ENUM ('jpg', 'jpeg', 'png', 'heic')")
    op.execute("CREATE TYPE imagestatus AS ENUM ('pending', 'uploaded', 'failed')")
    
    # Create images table
    op.create_table(
        'images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('file_type', postgresql.ENUM('jpg', 'jpeg', 'png', 'heic', name='imagetype', create_type=False), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('s3_key', sa.String(), nullable=False),
        sa.Column('s3_bucket', sa.String(), nullable=False),
        sa.Column('s3_url', sa.String(), nullable=True),
        sa.Column('status', postgresql.ENUM('pending', 'uploaded', 'failed', name='imagestatus', create_type=False), nullable=False, server_default='pending'),
        sa.Column('metadata', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    op.create_index(op.f('ix_images_user_id'), 'images', ['user_id'], unique=False)
    op.create_index(op.f('ix_images_s3_key'), 'images', ['s3_key'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_images_s3_key'), table_name='images')
    op.drop_index(op.f('ix_images_user_id'), table_name='images')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    
    # Drop table
    op.drop_table('images')
    
    # Drop enum types
    op.execute("DROP TYPE imagestatus")
    op.execute("DROP TYPE imagetype")

