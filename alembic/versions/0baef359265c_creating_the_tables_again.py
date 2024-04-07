"""creating the tables again

Revision ID: 0baef359265c
Revises: 9aebbd973a84
Create Date: 2024-04-06 10:55:41.367867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0baef359265c'
down_revision: Union[str, None] = '9aebbd973a84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyers',
    sa.Column('buyer_id', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), server_default='N/A', nullable=False),
    sa.Column('date_of_birth', sa.String(), server_default='N/A', nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('city', sa.String(), server_default='N/A', nullable=False),
    sa.Column('gender', sa.String(), server_default='N/A', nullable=False),
    sa.Column('country', sa.String(), server_default='N/A', nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_no', sa.String(), server_default='N/A', nullable=False),
    sa.Column('bought_fake', sa.String(), server_default='N/A', nullable=False),
    sa.Column('social_media_platform', sa.JSON(), nullable=True),
    sa.Column('is_scammed', sa.String(), server_default='N/A', nullable=False),
    sa.Column('use_venduit', sa.String(), server_default='N/A', nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('shopping', sa.String(), server_default='N/A', nullable=False),
    sa.Column('profile_picture', sa.String(), server_default='N/A', nullable=False),
    sa.Column('user_type', sa.String(), server_default='buyer', nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('buyer_id'),
    sa.UniqueConstraint('buyer_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('users',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id', 'email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('vendors',
    sa.Column('vendor_id', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), server_default='N/A', nullable=False),
    sa.Column('date_of_birth', sa.String(), server_default='N/A', nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), server_default='N/A', nullable=False),
    sa.Column('city', sa.String(), server_default='N/A', nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('phone_no', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_name', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_bio', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_category', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_reach', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_social_links', sa.JSON(), nullable=True),
    sa.Column('business_startDate', sa.String(), server_default='N/A', nullable=False),
    sa.Column('business_logo', sa.String(), server_default='N/A', nullable=False),
    sa.Column('is_scammed', sa.String(), server_default='N/A', nullable=False),
    sa.Column('use_venduit', sa.String(), server_default='N/A', nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('country', sa.String(), server_default='N/A', nullable=False),
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
    op.drop_table('users')
    op.drop_table('buyers')
    # ### end Alembic commands ###
