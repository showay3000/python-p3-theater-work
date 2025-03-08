"""empty message

Revision ID: 3e5ef4462ae6
Revises: 
Create Date: 2025-03-08 10:49:44.492282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e5ef4462ae6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'actors' table
    op.create_table(
        'actors',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
    )

    # Create the 'roles' table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('character_name', sa.String(), nullable=True),
    )

    # Create the 'auditions' table
    op.create_table(
        'auditions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('actor_id', sa.Integer(), sa.ForeignKey('actors.id'), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('hired', sa.Boolean(), nullable=True, default=False),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=True),
    )

def downgrade():
    # Drop the 'auditions' table
    op.drop_table('auditions')

    # Drop the 'roles' table
    op.drop_table('roles')

    # Drop the 'actors' table
    op.drop_table('actors')