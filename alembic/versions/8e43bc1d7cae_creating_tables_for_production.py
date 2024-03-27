"""creating tables for production

Revision ID: 8e43bc1d7cae
Revises: 743f3fb996a4
Create Date: 2024-03-27 09:10:10.147868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e43bc1d7cae'
down_revision: Union[str, None] = '743f3fb996a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyers',
    sa.Column('buyer_id', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_no', sa.String(), nullable=False),
    sa.Column('bought_fake', sa.String(), nullable=False),
    sa.Column('social_media_platform', sa.JSON(), nullable=True),
    sa.Column('is_scammed', sa.String(), nullable=False),
    sa.Column('use_venduit', sa.String(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('shopping', sa.String(), nullable=False),
    sa.Column('profile_picture', sa.String(), server_default='N/A', nullable=False),
    sa.Column('user_type', sa.String(), server_default='buyer', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('buyer_id'),
    sa.UniqueConstraint('buyer_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('vendors',
    sa.Column('vendor_id', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_no', sa.String(), nullable=False),
    sa.Column('business_name', sa.String(), nullable=False),
    sa.Column('business_bio', sa.String(), nullable=False),
    sa.Column('business_category', sa.String(), nullable=False),
    sa.Column('business_reach', sa.String(), nullable=False),
    sa.Column('business_social_links', sa.JSON(), nullable=True),
    sa.Column('business_startDate', sa.String(), nullable=False),
    sa.Column('business_logo', sa.String(), server_default='N/A', nullable=False),
    sa.Column('is_scammed', sa.String(), nullable=False),
    sa.Column('use_venduit', sa.String(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('profile_picture', sa.String(), server_default='N/A', nullable=False),
    sa.Column('user_type', sa.String(), server_default='vendor', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('vendor_id'),
    sa.UniqueConstraint('business_name'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('vendor_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendors')
    op.drop_table('buyers')
    # ### end Alembic commands ###