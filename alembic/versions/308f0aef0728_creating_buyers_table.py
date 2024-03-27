"""creating buyers table

Revision ID: 308f0aef0728
Revises: 514cf2e8d36a
Create Date: 2024-03-26 23:38:15.678932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '308f0aef0728'
down_revision: Union[str, None] = '514cf2e8d36a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('buyers')
    # ### end Alembic commands ###
