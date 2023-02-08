import sqlalchemy as sa
from convergent.db.metadata import METADATA

QUESTION = sa.Table(
    "question",
    sa.Column("date", sa.String, sa.ForeignKey("user.user_id")),
    sa.Column("question", sa.String),
)

ANSWER = sa.Table(
    "answer",
    sa.Column("user_id", sa.String, sa.ForeignKey("user.user_id")),
    sa.Column("answered", sa.Boolean),
)

USER = sa.Table("user", sa.Column("user_id", sa.String),)
