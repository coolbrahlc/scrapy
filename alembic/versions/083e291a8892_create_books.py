"""create books

Revision ID: 083e291a8892
Revises: 
Create Date: 2019-02-17 18:26:11.215794

"""
from alembic import op
import sqlalchemy as sa
import datetime
from sqlalchemy import DateTime


# revision identifiers, used by Alembic.
revision = '083e291a8892'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'books_table',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('book_url', sa.String(255), unique=True, nullable=False),
        sa.Column('book_created', sa.String(255), nullable=True),
        sa.Column('price', sa.Numeric(8, 2), nullable=True),
        sa.Column('currency', sa.String(20), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('available', sa.Integer(), nullable=True),
        sa.Column('genre', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('product_code', sa.String(255), nullable=True),
        sa.Column('product_type', sa.String(100), nullable=True),
        sa.Column('price_tax', sa.Numeric(8, 2), nullable=True),
        sa.Column('price_no_tax', sa.Numeric(8, 2), nullable=True),
        sa.Column('tax', sa.Numeric(8, 2), nullable=True),
        sa.Column('reviews_count', sa.Integer(), nullable=True),
        sa.Column('image_urls', sa.String(255), nullable=True),
        sa.Column('images', sa.String(255), nullable=True),
        sa.Column('created_at', DateTime, default=datetime.datetime.now),
        sa.Column('updated_at', DateTime, default=datetime.datetime.now)
    )



def downgrade():
    pass
