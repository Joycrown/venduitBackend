"""adjusting the tables

Revision ID: 6eda4fe342ab
Revises: 56021e8c9dd5
Create Date: 2024-04-06 09:57:51.470220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eda4fe342ab'
down_revision: Union[str, None] = '56021e8c9dd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'buyers', ['buyer_id'])
    op.create_unique_constraint(None, 'vendors', ['vendor_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vendors', type_='unique')
    op.drop_constraint(None, 'buyers', type_='unique')
    # ### end Alembic commands ###