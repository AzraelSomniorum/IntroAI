Define set_parameters():
    Initialize grid_size, steps, densities, hunger thresholds, and disaster parameters
    Return all parameters

Define count_neighbors(grid, x, y, layer):
    Initialize count = 0
    For each neighbor of (x, y):
        If neighbor is within bounds and grid[neighbor][layer] == 1:
            Increment count
    Return count

Define random_move(grid, x, y, layer):
    Shuffle move_directions = [up, down, left, right]
    For each direction in move_directions:
        Compute new_x, new_y with wrap-around grid limits
        If grid[new_x, new_y][layer] == 0:
            Move organism to new location
            Return new_x, new_y
    Return original x, y

Define update(grid, hunger levels, disaster_counter):
    Copy current grid to new_grid
    If random_chance < disaster_probability:
        Trigger disaster for disaster_duration

    For each cell (i, j) in the grid:
        # Grass dynamics
        For each grass_layer in [0, 1, 2]:
            If grid[i, j][grass_layer] == 1:
                If too many herbivores nearby:
                    Kill grass
            Else If enough neighboring grass:
                Grow new grass

        # Herbivore dynamics
        For each herbivore_layer in [3, 4, 5]:
            If grid[i, j][herbivore_layer] == 1:
                (i, j) = random_move(new_grid, i, j, herbivore_layer)
                If grass is nearby:
                    Eat grass and reset hunger
                Else:
                    Increment hunger
                    If hunger > threshold: Kill herbivore
                Check reproduction or overcrowding conditions

        # Carnivore dynamics
        For each carnivore_layer in [6, 7, 8]:
            If grid[i, j][carnivore_layer] == 1:
                (i, j) = random_move(new_grid, i, j, carnivore_layer)
                If herbivores are nearby:
                    Eat herbivore and reset hunger
                Else:
                    Increment hunger
                    If hunger > threshold: Kill carnivore
                Check reproduction or overcrowding conditions

    Return updated grid and hunger levels

Define draw(grid):
    For each cell (i, j) in grid:
        Map organisms (grass, herbivores, carnivores) to display colors
    Show the updated grid visualization

Define animate():
    For each step in simulation:
        Call update(grid, hunger levels, disaster_counter)
        Track populations of all organisms
        Call draw(grid)
        Update population graph visualization

Main program:
    Initialize parameters by calling set_parameters()
    Create grid and hunger arrays
    Populate grid with initial grass, herbivores, and carnivores
    Run animation for defined steps

-----------------------------------------------
----------------------------------------------

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
