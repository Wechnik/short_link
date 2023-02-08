"""initial

Revision ID: 1b84eca9e2d8
Revises: 
Create Date: 2023-02-07 16:48:24.199329

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b84eca9e2d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'short_link',
        sa.Column('hash', sa.String(length=15), unique=True, index=True),
        sa.Column('link', sa.String, unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.utcnow()),
    )


def downgrade():
    op.drop_table('short_link')
