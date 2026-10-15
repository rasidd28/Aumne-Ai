"""Initial posts table

Revision ID: 001
Revises: 
Create Date: 2026-10-14 21:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column(
            'status',
            sa.String(),
            nullable=False,
            server_default='draft',
        ),
        sa.Column('flagged_reasons', sa.Text(), nullable=True),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('draft','flagged','approved','published')",
            name='chk_posts_status'
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
