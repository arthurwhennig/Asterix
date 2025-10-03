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

- **Mode 2: Historical Impacts**
  - **UI**: A dropdown list of famous historical impact events.
  - **Options**: Chicxulub (Dinosaur Killer), Tunguska Event, Chelyabinsk Meteor.
  - **Interaction**: Selecting an event pre-fills the impactor parameters with historical estimates.

---

### Section 2: Select Target Location

- **Primary Action Button**: `"PINPOINT IMPACT ON GLOBE"`

**User Interaction Flow**:
1. User clicks the button, activating *Targeting Mode*. A crosshair appears on the screen.  
2. The user clicks a location on the 3D Cesium globe.  
3. This click triggers an asynchronous API call to the backend:  
   `POST /api/data-extraction/extract-async` with the selected latitude and longitude.  
4. The panel enters a loading state, displaying a checklist of the data being fetched in real-time:  
   - *Fetching Topography... ✓*  
   - *Querying Geology...*  

---

### Section 3: Target Analysis (Auto-Populated)

This read-only section populates with data once the backend extraction is complete. It confirms the properties of the impact site.

**Display Fields:**
- **Coordinates**: e.g., `30.31° N, 89.58° W`  
- **Surface Type**: `"Land Impact"` or `"Ocean Impact"`  
- **Elevation / Depth**: e.g., `-15 m (Coastal Plain)` or `-2,500 m (Ocean Floor)`  
- **Surface Geology**: e.g., `"Unconsolidated Sediment"` (from WFS query)  
- **Estimated Target Density**: e.g., `"1950 kg/m³"` (derived from geology)  

---

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
