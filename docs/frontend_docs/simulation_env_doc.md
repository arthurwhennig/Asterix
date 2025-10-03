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

### General Behavior and Layout

The right sidebar features a solid, opaque background, visually separating it from the main 3D viewport. Its color is a slightly lighter shade of the application's primary dark theme, ensuring text is highly readable while maintaining a cohesive, modern aesthetic.

By default, the Consequence Report panel remains collapsed on the right-hand side of the screen, appearing as a simple tab or handle to maximize the main view. When an impact event is simulated, the panel automatically expands to present its full analysis. Users can also manually expand or collapse this sidebar at any time.

The layout is organized vertically for clear readability. At the top is a static, non-collapsible "Brief Overview" that displays the most crucial data. Below this overview, a series of expandable sections, functioning like an accordion, allow the user to delve into more specific areas of the impact's aftermath.

If the sidebar content exceeds the screen height, the sidebar becomes vertically scrollable without affecting the rest of the UI.

### Section: Brief Overview

The "Brief Overview" section is permanently visible at the top of the expanded sidebar and provides the most critical details at a glance. This non-collapsible area contains key data points from the impact, including:

- **Impactor Profile**: i.e. key data about the size and composition of the asteroid.
- **Energy Release**: i.e. the amount of energy released in joules and megatones of TNT.
- **Crater Size**: i.e. the size of the crater caused by the impact.
- **Location**: i.e. it's location in relation to well-known ladmarks such as cities, etc.

### Expandable Sections: Detailed Analysis

Below the Brief Overview, the sidebar features several sections for in-depth analysis. These sections behave as an accordion: expanding one collapses the others, keeping focus on a single topic. Expanding a section pushes lower sections downward. If the content of the sidebar ends up taking more space than the sidebar height, the sidebar becomes scrollable (i.e., you can scroll through the sidebar without scrolling or moving things in the rest of the website).

**Interactive Key Terms**: Throughout the "Consequence Report," key scientific and technical terms will be displayed in italics. When a user hovers over one of these italicized terms for at least one second, a small, informative tooltip box will appear. This box will be positioned on the left side of the right sidebar, maintaining the same vertical alignment as the hovered term. It will provide a concise explanation, definition, or additional details about the term.

- **Seismic Analysis**
    - **Earthquake Magnitude**: Strength of the impact-induced quake (Richter scale).
    - **Shaking Intensity Zones**: Map of areas from light tremors to catastrophic shaking.

- **Social Analysis**
    - **Human Casualties**: Estimated fatalities and injuries.
    - **Population Displaced**: Estimated evacuees.

- **Economic Analysis**
    - **Destroyed Property**: Monetary value of destroyed homes, buildings, and infrastructure.
    - **Economic Disruption**: Regional and global economic impacts.
    - **Critical Infrastructure**: Impact to critical infrastructure systems.

- **Tsunami Analysis** (conditional: shown only for ocean/near-coast impacts)
    - **Initial Wave Height**: Size of the wave at the impact site.
    - **Tsunami Travel Time**: Map of arrival times to coastlines.
    - **Coastal Flooding**: Projected inland inundation extent.

- **Environmental Analysis**
    - **Atmospheric Dust & Cooling**: Estimated debris and potential cooling effects.
    - **Wildfire Radius**: Area ignited by thermal radiation.
    - **Damage to Nature**: Impacts to forests, wildlife, and ecosystems.

---

## 5. Bottom Bar: Master Controls

Contains the primary controls for running and reviewing the simulation.

- **Timeline**: Standard CesiumJS Timeline widget (play, pause, scrub).  
- **Primary Action Button**: Context-dependent large button (changes with application state).  

---
