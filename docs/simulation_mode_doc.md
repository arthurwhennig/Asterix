# Simulation Mode Interface Specification
## 1. Overview of Simulation Mode
    The Simulation Mode is the visualization phase where the user witnesses the consequences of their strategic defence configuration. Upon initiating the simulation, the system performs a one-time, high-fidelity physics calculation to determine the asteroid's new trajectory based on the forces exerted by the placed defence mechanisms.

    The user then observes a cinematic playback of this outcome. The simulation is not interactive; it is a visual report of the effectiveness of the user's plan. The playback is calibrated to last approximately 30 to 60 seconds at standard speed to provide a clear and compelling viewing experience.

## 2. Playback & Time Controls
    To give users control over their viewing experience, a persistent media control bar will be present at the bottom of the screen. This bar will include:

    - Play/Pause Button: A standard toggle button allowing the user to start and stop the simulation playback at any point.

    - Speed Adjustment: A button or dropdown menu to cycle through playback speeds: 1x (Normal), 2x, 3x, and 4x. This allows users to quickly advance to key moments or slow down to analyze specific interactions.

    - Timeline Scrubber: A visual progress bar showing the simulation's current point in time relative to its total duration. The user can drag this to jump to any point in the playback.

## 3. The Simulation Engine & Visuals
    The simulation is a two-step process: backend calculation followed by frontend visualization.

    ### 3.1. Trajectory Calculation
        Before visualization begins, the system's backend calculates the final, altered trajectory. This model is based on established principles of orbital mechanics, factoring in:

        - The asteroid's initial vector (speed, direction, mass, composition).

        - The gravitational pull of celestial bodies.

        - The precise forces applied by each user-placed defence item (e.g., the sustained, gentle pull of a gravity tractor or the sharp impulse from a kinetic impactor).

    ### 3.2. Visual Playback
        The user is shown a high-quality animation of the asteroid following this newly calculated path.

        - Successful Deflection: If the user's configuration successfully diverts the asteroid onto a trajectory that misses Earth, the simulation will show it flying safely past. The conclusion will be marked with a clear "Threat Neutralized" message.

        - Impact Scenario: If the defences are insufficient, the simulation will proceed to the impact event.

    ### 3.3. Impact Visualizations
        Should an impact occur, the system will generate a sequence of visualizations based on scientific models to illustrate the consequences.

        - Impact Location: The animation will show the asteroid striking the calculated geographic location (land or ocean).

        - Direct Consequences: A map overlay will appear, illustrating:

        - Crater Formation: A dynamically growing circle representing the final crater size.

        - Fireblast Radius: An expanding heat and pressure wave, showing the area of immediate, catastrophic destruction.

        - Secondary Consequences: The visualization will then show cascading effects:

        - Seismic Activity: Shockwaves will be shown radiating from the impact site, with data on the estimated magnitude of the resulting earthquakes.

        - Tsunamis: If the impact is in an ocean, the simulation will show the generation and propagation of tsunami waves across the globe.

        - Population Impact: Based on real-world population density data for the affected regions, the system will calculate and display an estimate of the human cost.

## 4. Post-Simulation Analysis & Scoring
    Once the simulation concludes (either via safe passage or impact), the user is taken to a Mission Debrief screen. This screen provides a comprehensive summary of their performance.

    - Mission Status: A clear and prominent banner declaring MISSION COMPLETED or MISSION FAILED.

    ###Performance Scorecard:

        - Economic Efficiency: The total cost of all deployed defence items.

        - Humanitarian Outcome: The estimated number of casualties (if an impact occurred). For a successful mission, this will be zero.

        - Final Score & Star Rating: For COMPLETED missions, a star rating from 1 to 3 is awarded based on efficiency:

            - ★☆☆ (Good): The threat was neutralized, but the cost was excessively high, indicating an inefficient "brute force" solution.

            - ★★☆ (Excellent): The threat was neutralized with a well-balanced and cost-effective defence configuration.

            - ★★★ (Perfect): A masterful solution. The threat was neutralized using the most optimal, lowest-cost configuration possible. This is the ultimate goal for players.

    This screen will feature clear calls to action, such as "Try Again" or "Modify Defence Plan," encouraging the user to iterate and perfect their strategy.