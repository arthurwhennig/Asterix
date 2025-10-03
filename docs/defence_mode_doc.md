# Defence Mode Interface Specification
## 1. Overview of Defence Mode
    The **Defence Mode** serves as the primary strategic planning phase for the user. In this interface, the user is presented with a static view of the impending threat, including the asteroid/meteor and its projected trajectory toward a target (e.g., Earth). This trajectory is displayed as a clear visual path, allowing the user to anticipate the object's movement over time.
    The core purpose of this mode is to allow the user to strategically place various defence mechanisms in space. It's important to note that placing these components will not alter the asteroid's trajectory in this planning view. The interface is purely for setup; the physical effects of the user's configuration will only be calculated and visualized once the simulation begins.
## 2. Defence Components & Budget
    All available defence mechanisms are treated as purchasable assets. Each component has an associated cost, reflecting its real-world manufacturing and deployment expenses. This cost is deducted from the user's total budget.
    A **Grand Total** or **Remaining Budget** counter will be prominently displayed in the top-right corner of the screen. This counter updates in real-time as the user adds, removes, or modifies their selection of defence components, providing immediate feedback on their spending.
## 3. The Shop Interface
    To access the defence hardware, the user can open the Shop.
    - Activation: The Shop is toggled via a clearly marked button, likely labeled "Shop" or "Defence Hardware," located in a main toolbar.
    - Appearance: When opened, the Shop appears as a persistent bar along the bottom of the screen.
    - Contents: This bar contains a catalog of all available defence items, such as Gravity Tractors, Kinetic Impulsers, and defensive Shields. Each item in the shop will display:
        - Its name and a small icon.
        - Its purchase cost.
        - A brief tooltip or pop-up description with key stats (e.g., effective range, power output, cooldown period) when hovered over.
## 4. Placement Workflow
    Placing a defence component is a straightforward, multi-step process designed for precision.
    - Selection: The user clicks on an item in the Shop to select it. Once selected, the item attaches to the user's cursor, often represented as a semi-transparent "ghost" image.
    - Rough Placement: The user moves their cursor to the desired location in space and clicks once to place the object. The object is now "staged" but not yet finalized.
    - Fine-Tuning: While an object is staged, the user can use the arrow keys on their keyboard to nudge it for precise positioning. Options for rotating the object could also be available during this step.
    - Confirmation: To finalize the placement, the user must click a green "Confirm" button, which will appear in the bottom-right of the screen. A red "Cancel" button will be present next to it to discard the current placement. Once confirmed, the cost is deducted, and the object is locked in place.
## 5. Configuration Management (Saving & Resetting)
    User progress is managed through a robust autosave and reset system.
    - Autosave: The user's current defensive configuration is automatically saved to our servers every time a change is made. This includes placing a new component, moving an existing one, or removing one. This ensures that progress is never lost during a session.
    - Reset Button: A "Reset Configuration" button will be available on the screen. Clicking this button will prompt the user with a confirmation dialog (e.g., "Are you sure you want to clear all placed items?") to prevent accidental deletion of their setup. If confirmed, the entire board is cleared, and the budget is returned to its starting value.
    - Data Storage Policy:
    - Un-run Configurations: Any defence setup that has not been run in a simulation will be saved for at least 24 hours.
    - Simulated Configurations: If a configuration is used to run a simulation, it is considered more important. We will permanently store the last 3 unique configurations that the user has simulated.
## 6. Running the Simulation
    When the user is satisfied with their defensive layout, they can initiate the simulation.

    A "Run Simulation" button will be located in the main UI, possibly next to the budget display. Clicking this button will transition the user from the static Defence Mode to the dynamic Simulation Mode. In this new mode, time begins to flow, the asteroid starts moving along its path, and all placed defence components become active, allowing the user to see the real-time consequences of their strategic decisions.
