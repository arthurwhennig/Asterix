# Data Extraction Services

This directory contains the automated data extraction services for the Asterix asteroid impact simulation platform. The services extract real-world data from various scientific sources to provide accurate impact simulation parameters.

## Overview

The data extraction system consists of several specialized extractors that gather data from different scientific sources:

1. **NASA JPL Extractor** - Asteroid characteristics from NASA's Small-Body Database
2. **Topography Extractor** - Elevation data from NASA's Common Metadata Repository
3. **Geology Extractor** - Geological data from OneGeology WFS services
4. **Regional Data Extractor** - Fault lines, bathymetry, population, and infrastructure data
5. **Impact Calculator** - Calculates impact effects using scientific formulas

## Architecture

```
api/services/
├── data_extraction.py          # Main orchestration service
├── impact_calculator.py        # Impact effect calculations
├── extractors/
│   ├── __init__.py
│   ├── nasa_jpl_extractor.py   # NASA JPL SBDB extractor
│   ├── topography_extractor.py # NASA CMR elevation extractor
│   ├── geology_extractor.py    # OneGeology WFS extractor
│   └── regional_data_extractor.py # Regional data extractor
└── README.md                   # This file
```

## Data Sources

### NASA JPL Small-Body Database (SBDB)
- **URL**: https://ssd-api.jpl.nasa.gov/sbdb.api
- **Data**: Asteroid diameter, velocity, mass, composition, orbital parameters
- **Method**: REST API with JSON response
- **Update Frequency**: Real-time

### NASA Common Metadata Repository (CMR)
- **URL**: https://cmr.earthdata.nasa.gov/stac/LPCLOUD
- **Data**: Digital elevation models, topography data
- **Method**: STAC (SpatioTemporal Asset Catalog) API
- **Collections**: COP-DEM_GLO-30-DGED, HLSL30, ASTER_GDEM_V003, SRTMGL1_v003

### OneGeology WFS Services
- **URL**: Various regional geological survey endpoints
- **Data**: Geological descriptions, rock types, densities
- **Method**: Web Feature Service (WFS) 2.0.0
- **Regions**: USGS, BGS, Geological Survey of Canada

### Regional Data Sources
- **Fault Lines**: Global Active Faults database from GEM Foundation
- **Bathymetry**: GEBCO global bathymetry grid
- **Population**: NASA SEDAC population density grids
- **Infrastructure**: OpenStreetMap data

## Usage

### Basic Data Extraction

```python
from api.services.data_extraction import DataExtractionService

# Create service instance
extraction_service = DataExtractionService(db_session)

# Extract comprehensive data
results = await extraction_service.extract_comprehensive_data(
    asteroid_name="Apophis",
    impact_latitude=39.7392,
    impact_longitude=-104.9903,
    impact_altitude=1600.0
)
```

### Individual Extractors

```python
# NASA JPL Extractor
from api.services.extractors.nasa_jpl_extractor import NASAJPLExtractor

async with NASAJPLExtractor() as extractor:
    asteroid_data = await extractor.extract_asteroid_data("Apophis")

# Topography Extractor
from api.services.extractors.topography_extractor import TopographyExtractor

async with TopographyExtractor() as extractor:
    elevation_data = await extractor.extract_elevation_data(39.7392, -104.9903)

# Geology Extractor
from api.services.extractors.geology_extractor import GeologyExtractor

async with GeologyExtractor() as extractor:
    geological_data = await extractor.extract_geological_data(39.7392, -104.9903)

# Regional Data Extractor
from api.services.extractors.regional_data_extractor import RegionalDataExtractor

async with RegionalDataExtractor() as extractor:
    regional_data = await extractor.extract_regional_data(39.7392, -104.9903, 100.0)
```

### Impact Calculations

```python
from api.services.impact_calculator import ImpactCalculator

calculator = ImpactCalculator()

impact_effects = calculator.calculate_impact_effects(
    asteroid_diameter_m=100.0,
    asteroid_velocity_ms=17000.0,
    asteroid_density_kg_m3=3000.0,
    target_density_kg_m3=2500.0,
    impact_latitude=39.7392,
    impact_longitude=-104.9903,
    elevation_m=1600.0,
    is_land=True
)
```

## API Endpoints

The data extraction services are exposed through REST API endpoints:

### Synchronous Extraction
```
POST /api/data-extraction/extract
Parameters:
- asteroid_name: string
- impact_latitude: float
- impact_longitude: float
- impact_altitude: float (optional)
```

### Asynchronous Extraction
```
POST /api/data-extraction/extract-async
Parameters:
- asteroid_name: string
- impact_latitude: float
- impact_longitude: float
- impact_altitude: float (optional)

Returns:
- extraction_id: string
- status_url: string
```

### Status Check
```
GET /api/data-extraction/status/{extraction_id}
Returns:
- status: string
- progress_percentage: float
- current_step: string
```

### Individual Data Sources
```
GET /api/data-extraction/asteroids/{asteroid_name}
GET /api/data-extraction/topography?latitude={lat}&longitude={lon}
GET /api/data-extraction/geology?latitude={lat}&longitude={lon}
GET /api/data-extraction/regional?latitude={lat}&longitude={lon}&radius_km={radius}
```

## Database Models

The extracted data is stored in the following database tables:

- `extraction_sessions` - Tracks extraction sessions
- `extracted_asteroid_data` - Asteroid characteristics
- `extracted_topography_data` - Elevation data
- `extracted_geological_data` - Geological information
- `extracted_regional_data` - Regional data (faults, population, etc.)
- `impact_calculations` - Calculated impact effects

## Error Handling

All extractors include comprehensive error handling:

- **Network errors**: Retry logic and fallback values
- **Data validation**: Coordinate bounds checking
- **API rate limits**: Respectful request pacing
- **Missing data**: Graceful degradation with defaults

## Performance Considerations

- **Async operations**: All extractors use async/await for non-blocking I/O
- **Connection pooling**: HTTP clients are reused across requests
- **Caching**: Results can be cached to avoid repeated API calls
- **Background processing**: Long-running extractions can be processed asynchronously

## Dependencies

The data extraction services require the following Python packages:

```
httpx>=0.25.2          # HTTP client for API requests
rasterio>=1.3.9        # Geospatial raster data processing
geopandas>=0.14.1      # Geospatial vector data processing
shapely>=2.0.2         # Geometric operations
pandas>=2.1.4          # Data manipulation
numpy>=1.24.4          # Numerical computing
pystac-client>=0.8.1   # STAC API client
```

## Configuration

Environment variables for data extraction:

```bash
# NASA API Configuration
NASA_API_KEY=your_nasa_api_key_here
NASA_API_BASE_URL=https://api.nasa.gov/neo/rest/v1

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/asterix_db

# Data Storage
DATA_DIR=./data  # Local data storage directory
```

## Testing

Each extractor includes test functions that can be run independently:

```bash
# Test NASA JPL extractor
python -m api.services.extractors.nasa_jpl_extractor

# Test topography extractor
python -m api.services.extractors.topography_extractor

# Test geology extractor
python -m api.services.extractors.geology_extractor

# Test regional data extractor
python -m api.services.extractors.regional_data_extractor

# Test impact calculator
python -m api.services.impact_calculator
```

## Contributing

When adding new extractors:

1. Create a new extractor class in the `extractors/` directory
2. Implement the async context manager pattern (`__aenter__`, `__aexit__`)
3. Add comprehensive error handling and logging
4. Include test functions for validation
5. Update the main `DataExtractionService` to integrate the new extractor
6. Add corresponding database models if needed
7. Update this README with the new extractor information

## License

This code is part of the Asterix project and is licensed under the MIT License.