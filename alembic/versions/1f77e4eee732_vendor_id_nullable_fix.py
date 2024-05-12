"""vendor_id nullable fix

Revision ID: 1f77e4eee732
Revises: 5e366c38f7cf
Create Date: 2024-04-15 15:25:57.187002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f77e4eee732'
down_revision: Union[str, None] = '5e366c38f7cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'vendor_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'vendor_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
