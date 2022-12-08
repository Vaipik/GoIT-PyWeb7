"""Init

Revision ID: 336b99410eef
Revises: 
Create Date: 2022-11-22 09:27:40.748465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '336b99410eef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('records',
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('record_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('tag_name')
    )
    op.create_table('emails',
    sa.Column('email_id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(length=50), nullable=True),
    sa.Column('record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['record_id'], ['records.record_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('email_id')
    )
    op.create_table('notes',
    sa.Column('note_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('edited_at', sa.DateTime(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.tag_id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('note_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('phones',
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.CHAR(length=10), nullable=True),
    sa.Column('record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['record_id'], ['records.record_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('phone_id'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phones')
    op.drop_table('notes')
    op.drop_table('emails')
    op.drop_table('tags')
    op.drop_table('records')
    # ### end Alembic commands ###