"""restructered_db

Revision ID: 781ef6be194a
Revises: 
Create Date: 2021-08-26 16:19:05.033970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '781ef6be194a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('superuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_superuser')),
    sa.UniqueConstraint('username', name=op.f('uq_superuser_username'))
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.Column('url_key', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('responsibilities', sa.String(), nullable=True),
    sa.Column('skills', sa.String(), nullable=True),
    sa.Column('is_full_time', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_part_time', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_fixed_term', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_permanent', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('status', sa.Enum('published', 'draft', 'cancelled', name='vacancy_status_enum'), server_default='published', nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_vacancy')),
    sa.UniqueConstraint('url_key', name=op.f('uq_vacancy_url_key'))
    )
    op.create_index(op.f('ix_vacancy_id'), 'vacancy', ['id'], unique=False)
    op.create_index(op.f('ix_vacancy_is_fixed_term'), 'vacancy', ['is_fixed_term'], unique=False)
    op.create_index(op.f('ix_vacancy_is_full_time'), 'vacancy', ['is_full_time'], unique=False)
    op.create_index(op.f('ix_vacancy_is_part_time'), 'vacancy', ['is_part_time'], unique=False)
    op.create_index(op.f('ix_vacancy_is_permanent'), 'vacancy', ['is_permanent'], unique=False)
    op.create_index(op.f('ix_vacancy_location'), 'vacancy', ['location'], unique=False)
    op.create_index(op.f('ix_vacancy_status'), 'vacancy', ['status'], unique=False)
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('cv_path', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('new', 'accepted', 'rejected', name='resume_status_enum'), server_default='new', nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('vac_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vac_id'], ['vacancy.id'], name=op.f('fk_resume_vac_id_vacancy'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_resume'))
    )
    op.create_index(op.f('ix_resume_id'), 'resume', ['id'], unique=False)
    op.create_index(op.f('ix_resume_status'), 'resume', ['status'], unique=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_resume_status'), table_name='resume')
    op.drop_index(op.f('ix_resume_id'), table_name='resume')
    op.drop_table('resume')
    op.drop_index(op.f('ix_vacancy_status'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_location'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_is_permanent'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_is_part_time'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_is_full_time'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_is_fixed_term'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_id'), table_name='vacancy')
    op.drop_table('vacancy')
    op.drop_table('superuser')
    # ### end Alembic commands ###