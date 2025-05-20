"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create learning_paths table
    op.create_table(
        'learning_paths',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_paths_id'), 'learning_paths', ['id'], unique=False)
    op.create_index(op.f('ix_learning_paths_title'), 'learning_paths', ['title'], unique=False)

    # Create learning_path_steps table
    op.create_table(
        'learning_path_steps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content_type', sa.Enum('text', 'video', 'quiz', 'exercise', name='contenttype'), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('learning_path_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['learning_path_id'], ['learning_paths.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_path_steps_id'), 'learning_path_steps', ['id'], unique=False)
    op.create_index(op.f('ix_learning_path_steps_title'), 'learning_path_steps', ['title'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_learning_path_steps_title'), table_name='learning_path_steps')
    op.drop_index(op.f('ix_learning_path_steps_id'), table_name='learning_path_steps')
    op.drop_table('learning_path_steps')
    op.drop_index(op.f('ix_learning_paths_title'), table_name='learning_paths')
    op.drop_index(op.f('ix_learning_paths_id'), table_name='learning_paths')
    op.drop_table('learning_paths')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users') 