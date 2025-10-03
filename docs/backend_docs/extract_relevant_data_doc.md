### Automated Data Extraction Roadmap for Impact Simulation
This document provides a detailed, step-by-step guide for the automated extraction of all data required to simulate the secondary consequences of a meteor impact. Each section outlines what data to get and how to get it programmatically.


## 1. Impactor Characteristics from NASA JPL
    This data defines the asteroid's physical and kinematic properties. We now use the JPL Horizons API for time-specific kinematics (e.g., velocity at a given epoch) and the SBDB API for static physical parameters when available.
### WHAT to Extract:
    Impactor Diameter: The asteroid's mean diameter in meters (m).
    Impactor Velocity (time-specific): The asteroid's speed at a requested epoch, in meters per second (m/s).
### HOW to Extract (Automated API Calls):
    - Identify Target Asteroid: Determine the official designation or numeric ID (e.g., "Apophis", "2000433").
    - Physical Parameters (Diameter/Mass/Composition) — SBDB API:
        - Base URL: https://ssd-api.jpl.nasa.gov/sbdb.api
        - Parameters:
            - sstr: The name/designation (e.g., sstr=Apophis)
            - phys-par=1: Request physical parameters
        - Example URL: https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=Apophis&phys-par=1
        - Parse JSON Response:
            - Diameter: `phys_par.diameter` (km) → convert to meters
            - Mass (if present): `phys_par.mass` (kg)
            - Composition/class (if present): e.g., `phys_par.spec_B`
    - Time-Specific Kinematics (Position/Velocity) — JPL Horizons API:
        - Base URL: https://ssd.jpl.nasa.gov/api/horizons.api
        - Parameters (query string):
            - format=text
            - COMMAND='ASTEROID_ID_OR_NAME' (e.g., '2000433')
            - OBJ_DATA=YES
            - MAKE_EPHEM=YES
            - EPHEM_TYPE=VECTORS
            - CENTER='500@0' (or desired center)
            - START_TIME='YYYY-MM-DD'
            - STOP_TIME='YYYY-MM-DD'
            - STEP_SIZE='1d' (or desired cadence)
        - Example URL: https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='2000433'&OBJ_DATA=YES&MAKE_EPHEM=YES&EPHEM_TYPE=VECTORS&CENTER='500@0'&START_TIME='2025-01-01'&STOP_TIME='2025-01-10'&STEP_SIZE='1d'
        - Parse Text Response:
            - Extract the ephemeris block between `$$SOE` and `$$EOE`
            - For each line, read position (X,Y,Z km) and velocity (VX,VY,VZ km/s)
            - Compute velocity magnitude and convert km/s → m/s as needed


## 2. Topography (Elevation) from NASA CMR
    This data provides the ground elevation at the impact site. It is retrieved using a query to a cloud-based data catalog.
### WHAT to Extract:
    - Ground Elevation: The elevation in meters (m) at the precise impact latitude and longitude.
### HOW to Extract (Automated Cloud Query):
    - Define Impact Coordinates: Specify the impact location as a latitude/longitude pair.
    - Connect to Data Catalog:
        -Use a STAC library (e.g., pystac_client in Python) to connect to the NASA Common Metadata Repository (CMR).
        - STAC Endpoint URL: https://cmr.earthdata.nasa.gov/stac/LPCLOUD
    - Search the Catalog:
        - Construct a search query for the catalog.
        - Collection: Specify the Copernicus Digital Elevation Model: "COP-DEM_GLO-30-DGED" or "HLSL30".
        - Filter: Use an intersects filter with the impact coordinates to find the specific data tile that covers your point.
    - Extract Data URL:
        - The search result will be a JSON object containing metadata.
        Navigate to assets and find the key for the data file (often named "COG" or "data").
        - Extract the href value. This is the direct URL to the cloud-hosted GeoTIFF file.
    - Read Value from Cloud:
        - Use a geospatial raster library (e.g., rasterio in Python) to open the URL.
        - Crucially, do not download the file. The library will stream the necessary information.
        - Use a sample or read function to request the single pixel value at your impact coordinates. The library handles the complex task of calculating which byte range to request from the server.
        - The returned value is the ground elevation in meters.


## 3. Geology (Target Density) from OneGeology
    This data defines the type of ground material at the impact site, which determines its density. It is retrieved by querying a Web Feature Service (WFS).
### WHAT to Extract:
    -Geological Description: A text string describing the surface material (e.g., "Cretaceous Sandstone").
    -Target Density: A numerical density value in kg/m³ derived from the description.
### HOW to Extract (Automated WFS Query):
    - Identify Regional WFS: For your area of interest, find the appropriate WFS endpoint URL and Layer Name from the OneGeology Portal. This is a one-time setup step.
    - Construct WFS Request:
        - Create a request to the WFS endpoint. This is typically a URL with several parameters.
        - Parameters:
            -service=WFS
            -version=2.0.0
            -request=GetFeature
            -typeName: The specific layer name you identified.
            -BBOX: A tiny bounding box created around your impact coordinates.
            -outputFormat: A standard format like GML3 or GeoJSON.
    -Execute API Call: Send a GET request to the WFS URL with the specified parameters.
    -Parse Response: The service will return an XML or JSON file containing data for the geological polygon at your location.
        -Parse the file to find the key containing the material description (e.g., ROCK_D, DESCRIPTION, UNIT_NAME).
    -Map Description to Density:
        -Use a function in your code to map the extracted text description to a density value.
        -Example Logic:
            -If description contains "granite" or "basalt" -> density = 2850 kg/m³.
            -If description contains "sandstone" or "limestone" -> density = 2400 kg/m³.
            -If description contains "clay" or "sand" -> density = 2000 kg/m³.


## 4. Supporting Regional Data (Local Query)
    This data is best handled by downloading a global or regional dataset once, saving it locally, and then querying it programmatically for each simulation.
    ###A. Fault Lines
        ### WHAT to Extract: The name and distance to the nearest active fault.
        ### HOW to Extract:
            - One-Time Download: Download the Global Active Faults database from the GEM Foundation as a shapefile.
            - Local Query: In your code, use a geospatial vector library (e.g., geopandas in Python) to load this local shapefile.
            - For each impact, calculate the distance from your coordinates to every fault feature and identify the minimum distance.
###B. Ocean Depth (Bathymetry)
    ### WHAT to Extract: Ocean depth in meters at the impact coordinates (if applicable).
    ### HOW to Extract:
        -One-Time Download: Download the GEBCO global bathymetry grid for your region.
        -Local Query: Use rasterio to open the local GEBCO file and read the pixel value at your coordinates.
###C. Population & Infrastructure
###WHAT to Extract: Population counts and locations of infrastructure within your calculated effect radii.
###HOW to Extract:
    - One-Time Download: Download population grids (from NASA SEDAC) and infrastructure vector data (from OpenStreetMap) for your region.
    - Local Analysis: After you calculate your consequence radii (e.g., the 5 PSI airblast ring), use geopandas and rasterio to perform a spatial analysis. This involves finding which population grid cells and infrastructure points/lines fall inside your effect polygons.
