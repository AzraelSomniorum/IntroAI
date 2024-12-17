### **1. Initial Setup**  
Function set_parameters():
    Define all parameters (grid size, initial densities, hunger limits, disaster settings)
    Return parameters as a dictionary

Create a 3D grid with 10 layers, where each layer represents:
    Layer 0-2: Grass types
    Layer 3-5: Herbivore types
    Layer 6-8: Carnivore types
    Layer 9: Unused (can be extended for other features)

Initialize grids for hunger tracking for herbivores and carnivores.
Randomly populate the grid based on initial densities.

---

### **2. Counting Surrounding Organisms**  

Function count_neighbors(grid, x, y, layer):
    Count the number of neighboring cells in a specific layer that are occupied.
    Skip out-of-bound cells and the current cell itself.
    Return the count of neighbors.

---

### **3. Random Movement**  
Function random_move(grid, x, y, layer):
    Randomly choose a direction (up, down, left, right).
    Check if the new position is empty (no same type or grass).
    Move the entity to the new position.
    Return the new coordinates.

---

### **4. Organism Behavior Rules**  
Function update(grid, hunger_grids, disaster_counter):
    If a random disaster occurs:
        Set disaster_counter to its duration.

For each grid cell (i, j):
        Update plants (layers 0-2):
            - Plants die if herbivores are nearby.
            - Regenerate plants under certain conditions (e.g., 3 neighbors).

Update herbivores (layers 3-5):
            - Move randomly.
            - If grass is nearby, eat grass and reset hunger.
            - If hunger exceeds a limit, the herbivore dies.
            - Reproduce under specific neighbor conditions.

Update carnivores (layers 6-8):
            - Move randomly.
            - If herbivores are nearby, eat herbivores and reset hunger.
            - If hunger exceeds a limit, the carnivore dies.
            - Reproduce under specific neighbor conditions.

Return updated grid, hunger grids, and disaster counter.

---

### **5. Visualization and Animation**  
Function draw(grid):
    Convert 3D grid into a 2D display grid with values:
        1: Grass1, 2: Grass2, 3: Grass3
        4-6: Herbivores, 7-9: Carnivores
    Display the grid using a custom color map.

Function animate(frame):
    Call the update function to process one simulation step.
    Track population counts for plants, herbivores, and carnivores.
    Update two plots:
        - Left: Grid visualization
        - Right: Population trends over time

---
### **6. Animation Execution**
Create animation using FuncAnimation:
    - Loop through `steps` number of frames.
    - Update the grid and visualization at each frame.
Show the animation.
