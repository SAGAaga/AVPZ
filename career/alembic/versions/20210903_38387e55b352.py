"""new enum columns in vacancy

Revision ID: 38387e55b352
Revises: 781ef6be194a
Create Date: 2021-09-03 13:35:08.280169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '38387e55b352'
down_revision = '781ef6be194a'
branch_labels = None
depends_on = None

def upgrade():
    job_type = postgresql.ENUM('full_time', 'part_time', name='vacancy_job_type_enum')
    job_type.create(op.get_bind())
    contract_type = postgresql.ENUM('fixed_term', 'permanent', name='vacancy_contract_type_enum')
    contract_type.create(op.get_bind())
    
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vacancy', sa.Column('job_type', sa.Enum('full_time', 'part_time', name='vacancy_job_type_enum'), nullable=True))
    op.add_column('vacancy', sa.Column('contract_type', sa.Enum('fixed_term', 'permanent', name='vacancy_contract_type_enum'), nullable=True))
    op.drop_index('ix_vacancy_is_fixed_term', table_name='vacancy')
    op.drop_index('ix_vacancy_is_full_time', table_name='vacancy')
    op.drop_index('ix_vacancy_is_part_time', table_name='vacancy')
    op.drop_index('ix_vacancy_is_permanent', table_name='vacancy')
    op.create_index(op.f('ix_vacancy_contract_type'), 'vacancy', ['contract_type'], unique=False)
    op.create_index(op.f('ix_vacancy_job_type'), 'vacancy', ['job_type'], unique=False)
    op.drop_column('vacancy', 'is_part_time')
    op.drop_column('vacancy', 'is_full_time')
    op.drop_column('vacancy', 'is_permanent')
    op.drop_column('vacancy', 'is_fixed_term')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vacancy', sa.Column('is_fixed_term', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('vacancy', sa.Column('is_permanent', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('vacancy', sa.Column('is_full_time', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('vacancy', sa.Column('is_part_time', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_vacancy_job_type'), table_name='vacancy')
    op.drop_index(op.f('ix_vacancy_contract_type'), table_name='vacancy')
    op.create_index('ix_vacancy_is_permanent', 'vacancy', ['is_permanent'], unique=False)
    op.create_index('ix_vacancy_is_part_time', 'vacancy', ['is_part_time'], unique=False)
    op.create_index('ix_vacancy_is_full_time', 'vacancy', ['is_full_time'], unique=False)
    op.create_index('ix_vacancy_is_fixed_term', 'vacancy', ['is_fixed_term'], unique=False)
    op.drop_column('vacancy', 'contract_type')
    op.drop_column('vacancy', 'job_type')
    job_type = postgresql.ENUM('full_time', 'part_time', name='vacancy_job_type_enum')
    job_type.drop(op.get_bind())
    contract_type = postgresql.ENUM('fixed_term', 'permanent', name='vacancy_contract_type_enum')
    contract_type.drop(op.get_bind())
    # ### end Alembic commands ###
