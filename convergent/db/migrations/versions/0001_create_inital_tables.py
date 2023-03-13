"""create_intial_tables

Revision ID: 0001
Revises: 
Create Date: 2022-10-08 15:30:50.987340

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def create_user_table():
    op.create_table(
        "users",
        sa.Column("user_id", sa.String, primary_key=True),
        sa.Column("password", sa.String),
        sa.Column("partner_id", sa.String),
    )


def create_answer_table():
    op.create_table(
        "answer",
        sa.Column("answer_id", sa.String, primary_key=True, default=str(uuid.uuid4),),
        sa.Column("date", sa.DATE, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.user_id"),),
        sa.Column("answered", sa.Boolean),
    )


def create_bible_table():
    op.create_table(
        "bible",
        sa.Column("book", sa.Integer, nullable=True),
        sa.Column("chapter", sa.Integer, nullable=True),
        sa.Column("versecount", sa.Integer, nullable=True),
        sa.Column("verse", sa.String(528), nullable=True),
    )


def upgrade():
    create_user_table()
    create_answer_table()
    create_bible_table()


def downgrade():
    op.drop_table("users")
    op.drop_table("answer")
    op.drop_table("bible")
