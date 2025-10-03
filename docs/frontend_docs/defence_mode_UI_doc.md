
# Frontend UI/UX Specification: Planetary Defense Mode

This document details the UI/UX for the **Planetary Defense Mode** of the Asterix platform.  
This mode transforms the impact viewer into an interactive, strategic simulation where users deploy assets to mitigate or prevent an asteroid impact.

---

## 1. Core Layout & Mode Transition

- **Mode Activation**: The user selects *Defense Mode* from the main header, which triggers a UI transition.  
  The color scheme shifts to a more urgent "alert" theme (e.g., amber or blue highlights), and the panel contents change.

- **Central Viewport**: The CesiumJS globe remains the central focus, but the initial view is zoomed out to a strategic, solar-system scale, showing Earth, the Moon, and the inbound asteroid's general trajectory.

---

## 2. Left Sidebar: Mission Briefing & Asset Deployment

This panel is the command center for the defense mission.

### Section 1: Threat Assessment

- **UI**: The user is presented with a list of pre-defined threat scenarios.

**Options:**  
- *Historical Threats*: Tunguska, Chelyabinsk (re-imagined as future threats).  
- *Future PHOs (Potentially Hazardous Objects)*: Apophis (2029 Flyby), Bennu (Future Risk).  

**Interaction:** Selecting a threat loads its data and displays its nominal trajectory—a dashed, ominous red line showing the potential path to an Earth impact.

**Targeting Control:** A slider labeled *"Adjust Impact Corridor"* allows the user to subtly modify the asteroid's trajectory to target different regions on Earth, creating varied challenges.

---

### Section 2: Strategic Asset Deployment

This is the core interactive component of Defense Mode.

- **Budget Display**: A prominent progress bar at the top of the panel shows the user's available budget (e.g., `$500B / $1,000B`).

- **Asset Arsenal**: A palette of available defense mechanisms, each with an icon, name, and cost.

#### Available Assets:

- 🚀 **Kinetic Impactor**: A sleek, arrow-like spacecraft.  
- 🔦 **Laser Ablation**: A high-tech satellite with a large primary mirror or phased array emitter.  
- 🛰️ **Gravity Tractor**: A bulky, powerful-looking spacecraft with prominent spherical masses.  

> **Deployment Interaction Flow**  
> - User clicks an asset from the arsenal (e.g., *"Kinetic Impactor"*).  
> - The selected asset’s box is surrounded by a **fading green highlight**, providing visual feedback for the current choice.  
> - The asset icon is attached to the mouse cursor.  
> - The user moves the cursor over the asteroid's trajectory line in the 3D view. The line highlights to show valid deployment zones.  
> - The user clicks on the trajectory to *place* the defense asset. A 3D model of the asset appears at that point in space, and the budget is deducted.  
> - The trajectory line instantly updates visually, showing a new, deflected path:  
>   - **Red** → Impact trajectory.  
>   - **Yellow** → Near miss.  
>   - **Green** → Safe trajectory.  
> - Multiple assets can be placed, further refining the asteroid’s path.

---

## 3. Central 3D Viewport: The Strategic View

- **Initial State**: Earth and Moon are visible. The asteroid's potential impact trajectory is shown as a dashed red line.  
  *(Final impact point is hidden – only the path is visible.)*

- **Placing Assets**: When a defense asset is deployed, its 3D model appears along the trajectory line.

- **Dynamic Trajectory Update**:  
  - A Gravity Tractor far from Earth → subtle bend in the path.  
  - A Kinetic Impactor closer to Earth → sharp “kink” in the line.  

- **Focus**: No cinematic impact visuals during planning; the emphasis is on orbital mechanics and trajectory changes.

---

## 4. Right Sidebar: Mission Success Prediction & Report Card

This panel provides predictive analysis during planning and a detailed, layered score after execution.

### Pre-Simulation: Predictive Analysis

- **Status Readout** (large, color-coded text):  
  - 🟥 *PREDICTED OUTCOME: DIRECT IMPACT*  
  - 🟨 *PREDICTED OUTCOME: NEAR MISS*  
  - 🟩 *PREDICTED OUTCOME: THREAT NEUTRALIZED*  

- **Predicted Impact Data** (if impact remains likely):  
  - Crater Size: ~8.5 km  
  - Quake: ~Mw 6.9  

### Post-Simulation: Mission Report Card

Triggered by the **EXECUTE DEFENSE PLAN** button.

**Section 1: Mission Summary (Always Visible)**  
- Outcome: *SUCCESS* / *FAILURE*  
- Final Score: ⭐ 0–3 stars  
- Justification text (e.g., “★★★ Perfect Score! Threat neutralized under budget.”)

**Performance Evaluation:**  
- Total Cost  
- Consequences Mitigated (e.g., `100% - Full Prevention`, `85% - Impact shifted to unpopulated ocean`).

**Section 2: Detailed Consequence Analysis (Expandable)**  
- Seismic: Magnitude, Shaking Zones  
- Social: Casualties, Displaced Population  
- Economic: Property Loss, Disruption  
- Tsunami (conditional): Wave Height, Coastal Flooding  
- Environmental: Dust, Wildfire Radius  

---

## 5. Bottom Bar: The Execution Button

- **Timeline**: Disabled during planning phase.  
- **Primary Action Button**:  
  - `EXECUTE DEFENSE PLAN`  
  - Locks in the choices, runs final simulation, and generates the Mission Report Card.
