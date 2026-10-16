
"""Complete user and recipe models

Revision ID: eb3ecdc5ce6f
Revises: b09e016836dc
Create Date: 2026-10-16 10:37:11.645785
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = 'eb3ecdc5ce6f'
down_revision = 'b09e016836dc'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns and relationship to recipes.
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('title', sa.String(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('instructions', sa.String(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('minutes_to_complete', sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('user_id', sa.Integer(), nullable=False)
        )
        batch_op.create_foreign_key(
            'fk_recipes_user_id_users',
            'users',
            ['user_id'],
            ['id']
        )

    # Add user profile and authentication columns.
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('username', sa.String(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('_password_hash', sa.String(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('image_url', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('bio', sa.String(), nullable=True)
        )
        batch_op.create_unique_constraint(
            'uq_users_username',
            ['username']
        )


def downgrade():
    # Remove user profile and authentication columns.
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_users_username',
            type_='unique'
        )
        batch_op.drop_column('bio')
        batch_op.drop_column('image_url')
        batch_op.drop_column('_password_hash')
        batch_op.drop_column('username')

    # Remove recipe columns and relationship.
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_recipes_user_id_users',
            type_='foreignkey'
        )
        batch_op.drop_column('user_id')
        batch_op.drop_column('minutes_to_complete')
        batch_op.drop_column('instructions')
        batch_op.drop_column('title')
