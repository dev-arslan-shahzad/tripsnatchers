"""age to date_of_birth

Revision ID: 2025_07_30_age_to_dob
Revises: 
Create Date: 2025-07-30 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_07_30_age_to_dob'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add date_of_birth column
    op.add_column('users', sa.Column('date_of_birth', sa.DateTime(), nullable=True))
    
    # Drop age column
    op.drop_column('users', 'age')

def downgrade():
    # Add age column back
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
    
    # Drop date_of_birth column
    op.drop_column('users', 'date_of_birth')
