import sqlalchemy as sa
from convergent.db.metadata import METADATA

ANSWER = sa.Table(
    "answer",
    METADATA,
    sa.Column("answer_id", sa.String),
    sa.Column("date", sa.DATE),
    sa.Column("user_id", sa.String, sa.ForeignKey("user.user_id")),
    sa.Column("answered", sa.Boolean),
)

USER = sa.Table(
    "users",
    METADATA,
    sa.Column("user_id", sa.String),
    sa.Column("password", sa.String),
    sa.Column("partner_id", sa.String),
)

BIBLE = sa.Table(
    "bible",
    METADATA,
    sa.Column("book", sa.Integer),
    sa.Column("chapter", sa.Integer),
    sa.Column("versecount", sa.Integer),
    sa.Column("verse", sa.String(528)),
)
