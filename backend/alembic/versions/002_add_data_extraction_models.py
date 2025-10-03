"""Add data extraction models

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create extraction_sessions table
    op.create_table('extraction_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_id', sa.String(), nullable=False),
        sa.Column('asteroid_name', sa.String(), nullable=False),
        sa.Column('impact_latitude', sa.Float(), nullable=False),
        sa.Column('impact_longitude', sa.Float(), nullable=False),
        sa.Column('impact_altitude', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('progress_percentage', sa.Float(), nullable=True),
        sa.Column('current_step', sa.String(), nullable=True),
        sa.Column('errors', sa.JSON(), nullable=True),
        sa.Column('warnings', sa.JSON(), nullable=True),
        sa.Column('data_sources', sa.JSON(), nullable=True),
        sa.Column('extraction_time_seconds', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extraction_sessions_extraction_id'), 'extraction_sessions', ['extraction_id'], unique=True)
    op.create_index(op.f('ix_extraction_sessions_id'), 'extraction_sessions', ['id'], unique=False)

    # Create extracted_asteroid_data table
    op.create_table('extracted_asteroid_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_session_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('nasa_id', sa.String(), nullable=False),
        sa.Column('diameter_m', sa.Float(), nullable=False),
        sa.Column('velocity_ms', sa.Float(), nullable=False),
        sa.Column('mass_kg', sa.Float(), nullable=True),
        sa.Column('composition', sa.String(), nullable=True),
        sa.Column('orbital_data', sa.JSON(), nullable=True),
        sa.Column('close_approach_data', sa.JSON(), nullable=True),
        sa.Column('is_potentially_hazardous', sa.Boolean(), nullable=True),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['extraction_session_id'], ['extraction_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_asteroid_name', 'extracted_asteroid_data', ['name'], unique=False)
    op.create_index('idx_extraction_session', 'extracted_asteroid_data', ['extraction_session_id'], unique=False)
    op.create_index('idx_nasa_id', 'extracted_asteroid_data', ['nasa_id'], unique=False)
    op.create_index(op.f('ix_extracted_asteroid_data_id'), 'extracted_asteroid_data', ['id'], unique=False)

    # Create extracted_topography_data table
    op.create_table('extracted_topography_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_session_id', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('elevation_m', sa.Float(), nullable=False),
        sa.Column('data_source', sa.String(), nullable=False),
        sa.Column('resolution_m', sa.Float(), nullable=True),
        sa.Column('confidence_level', sa.Float(), nullable=True),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['extraction_session_id'], ['extraction_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coordinates', 'extracted_topography_data', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_extraction_session', 'extracted_topography_data', ['extraction_session_id'], unique=False)
    op.create_index(op.f('ix_extracted_topography_data_id'), 'extracted_topography_data', ['id'], unique=False)

    # Create extracted_geological_data table
    op.create_table('extracted_geological_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_session_id', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('geological_description', sa.Text(), nullable=False),
        sa.Column('material_type', sa.String(), nullable=True),
        sa.Column('density_kg_m3', sa.Float(), nullable=False),
        sa.Column('age_period', sa.String(), nullable=True),
        sa.Column('formation_name', sa.String(), nullable=True),
        sa.Column('data_source', sa.String(), nullable=False),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['extraction_session_id'], ['extraction_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coordinates', 'extracted_geological_data', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_extraction_session', 'extracted_geological_data', ['extraction_session_id'], unique=False)
    op.create_index('idx_material_type', 'extracted_geological_data', ['material_type'], unique=False)
    op.create_index(op.f('ix_extracted_geological_data_id'), 'extracted_geological_data', ['id'], unique=False)

    # Create extracted_regional_data table
    op.create_table('extracted_regional_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_session_id', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('fault_name', sa.String(), nullable=True),
        sa.Column('fault_distance_km', sa.Float(), nullable=True),
        sa.Column('fault_type', sa.String(), nullable=True),
        sa.Column('fault_activity_status', sa.String(), nullable=True),
        sa.Column('fault_slip_rate', sa.Float(), nullable=True),
        sa.Column('depth_m', sa.Float(), nullable=True),
        sa.Column('is_land', sa.Boolean(), nullable=True),
        sa.Column('total_population', sa.Integer(), nullable=True),
        sa.Column('population_density_km2', sa.Float(), nullable=True),
        sa.Column('affected_area_km2', sa.Float(), nullable=True),
        sa.Column('major_cities', sa.JSON(), nullable=True),
        sa.Column('airports', sa.JSON(), nullable=True),
        sa.Column('ports', sa.JSON(), nullable=True),
        sa.Column('power_plants', sa.JSON(), nullable=True),
        sa.Column('hospitals', sa.JSON(), nullable=True),
        sa.Column('schools', sa.JSON(), nullable=True),
        sa.Column('extracted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['extraction_session_id'], ['extraction_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coordinates', 'extracted_regional_data', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_extraction_session', 'extracted_regional_data', ['extraction_session_id'], unique=False)
    op.create_index(op.f('ix_extracted_regional_data_id'), 'extracted_regional_data', ['id'], unique=False)

    # Create impact_calculations table
    op.create_table('impact_calculations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('extraction_session_id', sa.Integer(), nullable=True),
        sa.Column('impact_energy_joules', sa.Float(), nullable=False),
        sa.Column('impact_energy_megatons', sa.Float(), nullable=False),
        sa.Column('crater_diameter_km', sa.Float(), nullable=False),
        sa.Column('crater_depth_km', sa.Float(), nullable=False),
        sa.Column('fireball_radius_km', sa.Float(), nullable=True),
        sa.Column('thermal_radiation_radius_km', sa.Float(), nullable=True),
        sa.Column('blast_wave_radius_km', sa.Float(), nullable=True),
        sa.Column('richter_magnitude', sa.Float(), nullable=True),
        sa.Column('tsunami_wave_height_meters', sa.Float(), nullable=True),
        sa.Column('calculation_method', sa.String(), nullable=True),
        sa.Column('calculation_version', sa.String(), nullable=True),
        sa.Column('calculation_metadata', sa.JSON(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['extraction_session_id'], ['extraction_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_extraction_session', 'impact_calculations', ['extraction_session_id'], unique=False)
    op.create_index('idx_impact_energy', 'impact_calculations', ['impact_energy_joules'], unique=False)
    op.create_index(op.f('ix_impact_calculations_id'), 'impact_calculations', ['id'], unique=False)


def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_impact_calculations_id'), table_name='impact_calculations')
    op.drop_index('idx_impact_energy', table_name='impact_calculations')
    op.drop_index('idx_extraction_session', table_name='impact_calculations')
    op.drop_table('impact_calculations')

    op.drop_index(op.f('ix_extracted_regional_data_id'), table_name='extracted_regional_data')
    op.drop_index('idx_extraction_session', table_name='extracted_regional_data')
    op.drop_index('idx_coordinates', table_name='extracted_regional_data')
    op.drop_table('extracted_regional_data')

    op.drop_index(op.f('ix_extracted_geological_data_id'), table_name='extracted_geological_data')
    op.drop_index('idx_material_type', table_name='extracted_geological_data')
    op.drop_index('idx_extraction_session', table_name='extracted_geological_data')
    op.drop_index('idx_coordinates', table_name='extracted_geological_data')
    op.drop_table('extracted_geological_data')

    op.drop_index(op.f('ix_extracted_topography_data_id'), table_name='extracted_topography_data')
    op.drop_index('idx_extraction_session', table_name='extracted_topography_data')
    op.drop_index('idx_coordinates', table_name='extracted_topography_data')
    op.drop_table('extracted_topography_data')

    op.drop_index(op.f('ix_extracted_asteroid_data_id'), table_name='extracted_asteroid_data')
    op.drop_index('idx_nasa_id', table_name='extracted_asteroid_data')
    op.drop_index('idx_extraction_session', table_name='extracted_asteroid_data')
    op.drop_index('idx_asteroid_name', table_name='extracted_asteroid_data')
    op.drop_table('extracted_asteroid_data')

    op.drop_index(op.f('ix_extraction_sessions_id'), table_name='extraction_sessions')
    op.drop_index(op.f('ix_extraction_sessions_extraction_id'), table_name='extraction_sessions')
    op.drop_table('extraction_sessions')
