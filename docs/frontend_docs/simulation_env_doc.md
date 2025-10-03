# Frontend UI/UX Specification: Meteor Madness Impact Viewer

This document outlines the UI/UX for a web-based, 3D interactive application designed for the **"Meteor Madness"** challenge. The interface is built on **CesiumJS** and is focused exclusively on the selection, simulation, and detailed analysis of a meteor impact on Earth, leveraging backend data extraction and calculation services.

---

## 1. Core Application Layout

The interface is designed as a full-screen **Planetary Situation Room** with a central 3D globe viewport and collapsible side panels for controls and data analysis.

**Layout Components:**
- **Main 3D Viewport**: A dominant, interactive CesiumJS globe.  
- **Left Sidebar (Collapsible)**: The *Scenario Hub* for defining the impact parameters.  
- **Right Sidebar (Collapsible)**: The *Consequence Report* for displaying detailed post-impact analysis.  
- **Bottom Bar**: A master timeline for controlling the simulation playback.  

---

## 2. Left Sidebar: The Scenario Hub

This is the user's primary control panel for setting up the entire simulation. It guides the user through selecting an impactor and a target location.

### Section 1: Select Impactor

This section allows the user to choose the threat object from two sources.

- **Mode 1: Real-Time NEO (Near-Earth Object)**
  - **UI**: A searchable, filterable list of current NEOs, populated by a call to the backend's asteroid data endpoint.
  - **Data Displayed**: Each list item shows the asteroid's **Name**, **Diameter (km)**, and **Is Hazardous** status.
  - **Interaction**: Clicking an asteroid selects it for the simulation.


## 3. Central 3D Viewport & Simulation Visuals

The heart of the application, where the entire event unfolds.

**Visualization of the Event:**
- **Trajectory**: A `PolylineGraphics` entity shows the asteroid's calculated path.  
- **Atmospheric Entry**: Below 100 km altitude, the asteroid model gains a bright, fiery emissive material and a particle trail.  
- **Impact Flash**: A brilliant `BillboardGraphics` flare saturates the impact point at T-0.  
- **Crater**: A textured `PolygonGraphics` dynamically drawn on the terrain, with diameter from backend calculation.  
- **Airblast Rings**: Semi-transparent, expanding `EllipseGraphics` rings for 1, 5, and 10 PSI, fading over time.  
- **Seismic Visualization**: A **USGS ShakeMap** overlay for ground-shaking intensity, draped on the globe.  

---

## 4. Right Sidebar: The Consequence Report

This panel is initially collapsed and expands upon impact to provide a detailed, multi-tabbed analysis of the consequences.

### Tab 1: Executive Summary
- **Energy Release**: Kinetic Energy (Joules) and TNT Equivalent (Megatons).  
- **Primary Physical Effects**: Crater Diameter (km), Earthquake Magnitude (Mw).  
- **Human Impact Overview**: e.g., *"Catastrophic damage expected within a 50 km radius. Significant tsunami risk for adjacent coastlines."*  

### Tab 2: Airblast Analysis
- **Damage Radii**: Breakdown of distances for each PSI threshold.  
- **Interactive Chart**: Overpressure (PSI) vs. Distance (km).  
- **Infrastructure Report**: Scrollable list of cities, airports, and power plants within damage rings.  

### Tab 3: Seismic Analysis
- **ShakeMap Legend**: Explains the color-coding of seismic intensity.  
- **Fault Proximity**: e.g., *"Impact is 75 km from the San Andreas Fault."*  

### Tab 4: Tsunami Analysis *(Ocean Impacts Only)*
- **Wave Propagation Model**: Estimated tsunami arrival times at coastlines.  
- **Inundation Risk**: List of high-risk coastal areas where wave height exceeds DEM elevation.  

---

## 5. Bottom Bar: Master Controls

Contains the primary controls for running and reviewing the simulation.

- **Timeline**: Standard CesiumJS Timeline widget (play, pause, scrub).  
- **Primary Action Button**: Context-dependent large button (changes with application state).  

---
