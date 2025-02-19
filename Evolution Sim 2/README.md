# Evolution Simulator

## Overview
This is a grid-based evolution simulator built using Python and Raylib. The simulation models a dynamic ecosystem where entities compete for survival, evolve through mutations, and adapt over generations.

## Features
- **Grid-Based Movement**: Entities navigate a structured grid.
- **Entity Classes**:
  - Assassin: Small, fast, high vision.
  - Norms: Balanced stats.
  - Tanks: Large, strong, low vision.
- **Stats & Progression**:
  - Hunger, Vision, Speed, Strength, and Age affect survival.
  - Entities grow from childhood to adulthood, impacting stats.
- **Behavior & AI**:
  - Entities search for food using vision and scent.
  - They avoid or engage in combat based on size and strength.
  - Reproduction occurs with inherited traits and mutations.
- **Food Mechanics**:
  - Food spawns in clusters and emits a scent that fades over time.
  - Entities locate food via sight or scent before it rots.
- **UI & Visualization**:
  - Adjustable game speed and pause menu.
  - Hovering over entities displays stats.
  - Data collection and visualization of evolutionary progress.

## Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/evolution-simulator.git
   cd evolution-simulator
   ```
2. Install dependencies:
   ```sh
   pip install raylib == 5.5.0.2
   ```
3. Run the simulation:
   ```sh
   python main.py
   ```
   
![Simulation Preview](https://github.com/UdeaghaXavier/Raylib/blob/main/Evolution%20Sim%202/Assets/simulation.gif)


## Contribution
Feel free to contribute by opening issues, submitting pull requests, or suggesting improvements!

## License
[MIT License](LICENSE)

