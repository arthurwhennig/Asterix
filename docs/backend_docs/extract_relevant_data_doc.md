# Sources to extract from
## NASA NEO API 
### JPL Small-Body Database (SBDB) API
    - Impactor diameter: estimated size of asteroid : 
        - API Field: Look for the "diameter" field in the phys_par (physical parameters) section of the API's JSON response.
        - Details: This value is typically given in kilometers (km), so this must be converedt to meters for your volume and mass calculations. Often, a range is provided; using the nominal or average value is a good approach.
    - Impactor velocity: asteroids speed relative to earth
        - API Field: Look for the "v_rel" field within the ca_data (close-approach data) section of the API response.
        - Details: This value represents the relative velocity and is given in kilometers per second (km/s). This must be converted to meters per second (m/s) for the kinetic energy formula.

## USgS 
    - Geological Maps: Extract the target surface density (e.g., rock, soil) for the chosen impact location.
    - Digital Elevation Models (DEMs): Get high-resolution elevation data for the area. This is critical for modeling tsunami inundation and airblast effects over terrain.
    - Fault Line Maps: Extract the locations of nearby seismic faults to analyze the potential for triggered earthquakes.
    - PAGER (Prompt Assessment of Global Earthquakes for Response): Use this system to model the ground shaking and potential damage after you calculate the earthquake's magnitude.
## NOAA
    - Bathymetry Data (e.g., GEBCO datasets): Extract the ocean depth at the exact point of impact. This is crucial for the tsunami wave calculation.
## NASA SEDAC
    - population data for regions that the effects will cover 
## needed without current source
    - Infrastructure Data (e.g., from OpenStreetMap or specific government portals): Extract the locations of cities, roads, power plants, and other critical structures.