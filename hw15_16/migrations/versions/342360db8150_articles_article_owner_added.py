"""articles article owner added

Revision ID: 342360db8150
Revises: 0beeafb33e64
Create Date: 2023-01-19 10:52:51.482614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "342360db8150"
down_revision = "0beeafb33e64"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "articles", sa.Column("owner", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.create_foreign_key(
        None, "articles", "users", ["owner"], ["uuid"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "articles", type_="foreignkey")
    op.drop_column("articles", "owner")
    # ### end Alembic commands ###
