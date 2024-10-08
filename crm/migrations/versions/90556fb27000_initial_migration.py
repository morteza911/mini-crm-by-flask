"""Initial migration

Revision ID: 90556fb27000
Revises: 
Create Date: 2024-09-21 15:34:50.648661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90556fb27000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('family', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('campaign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('address', sa.String(length=230), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('phone_number_two', sa.String(length=15), nullable=True),
    sa.Column('phone_number_three', sa.String(length=15), nullable=True),
    sa.Column('fax', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=60), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('family', sa.String(length=30), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('phone_number_two', sa.String(length=15), nullable=True),
    sa.Column('phone_number_three', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('negotiation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=30), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.Column('stage_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['stage_id'], ['stage.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('negotiation_id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_registration', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['negotiation_id'], ['negotiation.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('visit_date', sa.DateTime(), nullable=False),
    sa.Column('negotiation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['negotiation_id'], ['negotiation.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('record')
    op.drop_table('negotiation')
    op.drop_table('customer')
    op.drop_table('company')
    op.drop_table('campaign')
    op.drop_table('user')
    op.drop_table('stage')
    op.drop_table('activity')
    # ### end Alembic commands ###
