"""creating an order item table

Revision ID: 47d77d6852a5
Revises: 1f77e4eee732
Create Date: 2024-04-28 23:50:21.008447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47d77d6852a5'
down_revision: Union[str, None] = '1f77e4eee732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.String(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('product_desc', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('product_image', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    op.drop_constraint('orders_order_id_key', 'orders', type_='unique')
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=True)
    op.drop_column('orders', 'product_desc')
    op.drop_column('orders', 'product_name')
    op.drop_column('orders', 'quantity')
    op.drop_column('orders', 'price')
    op.drop_column('orders', 'product_image')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('product_image', sa.VARCHAR(), server_default=sa.text("'N/A'::character varying"), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('price', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('product_desc', sa.VARCHAR(), server_default=sa.text("'N/A'::character varying"), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.create_unique_constraint('orders_order_id_key', 'orders', ['order_id'])
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')
    # ### end Alembic commands ###
