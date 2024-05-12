"""creating the order and dispute table

Revision ID: 52bca1f0f29c
Revises: d46d627eef9b
Create Date: 2024-04-14 13:27:43.342959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52bca1f0f29c'
down_revision: Union[str, None] = 'd46d627eef9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'disputes', ['dispute_id'])
    op.create_unique_constraint(None, 'orders', ['order_id'])
    op.drop_constraint('orders_buyer_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'buyers', ['buyer_id'], ['buyer_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_buyer_id_fkey', 'orders', 'users', ['buyer_id'], ['user_id'])
    op.drop_constraint(None, 'orders', type_='unique')
    op.drop_constraint(None, 'disputes', type_='unique')
    # ### end Alembic commands ###
