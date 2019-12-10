"""empty message

Revision ID: e351f6d5cd71
Revises: 0cccf6a5348b
Create Date: 2019-12-09 17:46:32.930515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e351f6d5cd71'
down_revision = '0cccf6a5348b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Game',
    sa.Column('img_name', sa.String(length=64), nullable=False),
    sa.Column('word_subject', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['word_subject'], ['WordSubject.wordsubject'], ),
    sa.PrimaryKeyConstraint('img_name')
    )
    op.create_index(op.f('ix_Game_img_name'), 'Game', ['img_name'], unique=True)
    op.create_table('game_word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('h', sa.Integer(), nullable=True),
    sa.Column('w', sa.Integer(), nullable=True),
    sa.Column('word', sa.String(length=64), nullable=True),
    sa.Column('word_subject', sa.String(length=64), nullable=True),
    sa.Column('game_img', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['game_img'], ['Game.img_name'], ),
    sa.ForeignKeyConstraint(['word'], ['Word.word'], ),
    sa.ForeignKeyConstraint(['word_subject'], ['WordSubject.wordsubject'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('User', 'member_since')
    op.drop_column('User', 'location')
    op.drop_column('User', 'id')
    op.drop_column('User', 'last_seen')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    op.add_column('User', sa.Column('id', sa.INTEGER(), nullable=True))
    op.add_column('User', sa.Column('location', sa.VARCHAR(length=64), nullable=True))
    op.add_column('User', sa.Column('member_since', sa.DATETIME(), nullable=True))
    op.drop_table('game_word')
    op.drop_index(op.f('ix_Game_img_name'), table_name='Game')
    op.drop_table('Game')
    # ### end Alembic commands ###