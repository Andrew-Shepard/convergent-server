"""create_intial_tables

Revision ID: 0001
Revises: 
Create Date: 2022-10-08 15:30:50.987340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def create_user_table():
    op.create_table(
        "user",
        sa.Column("user_id", sa.String, primary_key=True),
        sa.Column("detail", sa.String),
    )


def create_answer_table():
    op.create_table(
        "answer",
        sa.Column("answer_id",sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("user.user_id")),
        sa.Column("answered", sa.Boolean),
    )


def create_question_table():
    op.create_table(
        "question", sa.Column("date", sa.TIMESTAMP), sa.Column("question", sa.String),
    )


def upgrade():
    create_user_table()
    # create_question_table()
    # create_answer_table()


def downgrade():
    op.drop_table("user")
    op.drop_table("answer")
    op.drop_table("question")
