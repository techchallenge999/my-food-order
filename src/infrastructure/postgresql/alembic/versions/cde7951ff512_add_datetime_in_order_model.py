"""add datetime in order model

Revision ID: cde7951ff512
Revises: 966b0d48a72f
Create Date: 2023-07-08 03:29:25.839082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cde7951ff512"
down_revision = "966b0d48a72f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "order",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "order",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order", "updated_at")
    op.drop_column("order", "created_at")
    # ### end Alembic commands ###
