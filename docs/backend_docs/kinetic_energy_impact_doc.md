We want to use the USGS data sets to approximate secondary impact consequences:
Data we will need to provide:
### impactor characteristics:
    - diameter of the impactor 
    - impactor velocity relative to earth
    - density of the impactor 
### target properties:
    - target type (land or water)
    - target density 
    - water depth
### Geospatial Consequence Data
    - Topography/Elevation Data: High-resolution Digital Elevation Models (DEMs) are needed for both land and coastal areas. On land, they help model how terrain affects the airblast. For tsunamis, they are crucial for modeling which low-lying coastal areas will be flooded.
    - Infrastructure & Population Data: To quantify the damage, you need maps showing the locations of cities, roads, critical facilities (hospitals, power plants), and population density.
    - Geological Data: Maps of fault lines are needed to analyze how the impact's seismic shock might interact with pre-existing geological stress.


## Calculate the kinetic impact energy and use the USGS data sets to model secondary consequences:
    - approximate radius 
    - find volume 
    - use density to find the mass 
    - use the impact velocity to approximate the kinetic energy 
formulas:
radius = diameter / 2
Volume = 4/3 * radius^3 * pi
mass = density * volume
kinetic energy = 1/2 * mass * (impact_velocity)^2 

## Crater
Holsapple-Schmidt   
crater Dimensions = 1.161 * ((impactor density) / (target surface density))^(1/3) ((kinetic energy)/(target melting energy))^(0.22) (impactor diameter)

## Airblast effects:
### damage thresholds:
1 psi: most windows shatter 
2-3 psi: most residential buildings are severely damaged 
5 psi: most buildings destroyed 
10-20 psi: reinforced concrete buildings severly damaged 
### formula:
overpressure = 0.85 * (kinetic energy)^(1/3) / range + 3 *  (kinetic energy)^(2/3) / range^2 + 7  (kinetic energy) / range^3


### Earthquake
M_w := Moment magnitude 
KE = kinetic energy of impactor 

M_w = 0.67 * log_10(KE) - 5.87

Then we will use the USGS shake base maps (like PAGER) to estimate the intensity of ground shaking at various distances from the impact epicenter the chosen geolocation

## Tsunami generation 
If the impact occurs in an ocean, it will generate a tsunami. The properties of the wave depend on the crater size in the seafloor and the ocean depth

First, calculate the crater Dimension(denoted D_c) using the formula above. We can estimate the height of the wave (denoted H) and the distance from the impact location(denoted r). 
Further d denotes the depth of the water at the impact location. 
H = 0.15((D_c^4)/ (d^2 * r^2))^(1/4)

We will use the data from the NOAA and USGS to find or approximate the parameters needed for the above calculation. 

After calculating the initial wave height (H) at a distance (r), we will use USGS high-resolution coastal DEMs. By identifying the coastal areas where the predicted wave height exceeds the land elevation, we can map the potential inundation zone. We will then overlay this zone with infrastructure and population data to approximate the consequences."