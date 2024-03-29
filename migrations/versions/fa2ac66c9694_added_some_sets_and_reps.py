"""added some sets and reps

Revision ID: fa2ac66c9694
Revises: 49316a9a0a22
Create Date: 2024-02-08 19:05:18.056276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa2ac66c9694'
down_revision = '49316a9a0a22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('cust_id', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('cust_id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.String(), nullable=False),
    sa.Column('order_total', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('prod_order',
    sa.Column('prodorder_id', sa.String(), nullable=False),
    sa.Column('prod_id', sa.String(), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=False),
    sa.Column('sets', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('order_id', sa.String(), nullable=False),
    sa.Column('cust_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['cust_id'], ['customer.cust_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.ForeignKeyConstraint(['prod_id'], ['product.prod_id'], ),
    sa.PrimaryKeyConstraint('prodorder_id')
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('sets',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('sets',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=10, scale=2),
               existing_nullable=False)

    op.drop_table('prod_order')
    op.drop_table('order')
    op.drop_table('customer')
    # ### end Alembic commands ###
