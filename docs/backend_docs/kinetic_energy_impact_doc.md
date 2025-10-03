We want to use the USGS data sets to approximate secondary impact consequences:
Data we will need to provide:
    - approximate geolocation
    - 








- Calculate the kinetic impact energy and use the USGS data sets to model secondary consequences:
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

Then we will use the USGS shake base maps (like PAGER) to estimate the intensity of ground shaking at various distances from the impact epicenter your chosen geolocation

