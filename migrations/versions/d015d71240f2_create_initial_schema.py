"""create initial schema

Revision ID: d015d71240f2
Revises: 
Create Date: 2021-11-19 22:20:28.240431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd015d71240f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create the initial tables to persist each avenger, their deaths, and any log information
    """
    op.create_table(
        "avengers",

        sa.Column("id", sa.BigInteger, primary_key=True),

        sa.Column("url", sa.Unicode(255)),
        sa.Column("name", sa.Unicode(255)),
        sa.Column("appearances", sa.BigInteger, nullable=False),
        sa.Column("current", sa.Boolean, nullable=False),
        sa.Column("gender", sa.Unicode(50)),
        sa.Column("probationary", sa.Date),
        sa.Column("full_reserve", sa.Date),
        sa.Column("year", sa.BigInteger),
        sa.Column("honorary", sa.Unicode(50)),
        sa.Column("notes", sa.UnicodeText)
    )

    op.create_table(
        "deaths",

        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("avenger_id", sa.BigInteger, sa.ForeignKey("avengers.id"), nullable=False),

        sa.Column("death", sa.Boolean),
        sa.Column("returned", sa.Boolean),
        sa.Column("sequence", sa.BigInteger, nullable=False)
    )
    op.create_index("idx_deaths_avengers_id", "deaths", ["avenger_id"])

    op.create_table(
        "logs",

        sa.Column("id", sa.BigInteger, primary_key=True),

        sa.Column("context_id", sa.BigInteger),
        sa.Column("context_type", sa.Unicode(255)),

        sa.Column("what", sa.Unicode(255), nullable=False),
        sa.Column("who", sa.Unicode(255), nullable=False),
        sa.Column("when", sa.DateTime, nullable=False),

        sa.Column("custom1", sa.UnicodeText),
        sa.Column("custom2", sa.UnicodeText),
        sa.Column("custom3", sa.UnicodeText)
    )
    op.create_index("idx_logs_context", "logs", ["context_id", "context_type"])


def downgrade():
    """
    Drop all of the tables created in the initial schema
    """
    op.drop_table("deaths")
    op.drop_table("avengers")
    op.drop_table("logs")
