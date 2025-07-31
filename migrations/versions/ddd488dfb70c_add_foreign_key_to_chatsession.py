"""Add foreign key to ChatSession

Revision ID: ddd488dfb70c
Revises: af8fa7460019
Create Date: 2025-07-22 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ddd488dfb70c'
down_revision = 'af8fa7460019'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_chat_message_chat_session_id',  # <--- Explicit name here
            'chat_session',                     # Referenced table
            ['chat_session_id'],                # Local columns
            ['id']                             # Remote columns
        )


def downgrade():
    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_chat_message_chat_session_id', type_='foreignkey')
