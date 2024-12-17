```python
def set_parameters():
    params = {
        "grid_size": 100,
        "steps": 200,
        "initial_grass1_density": 0.2,
        "initial_grass2_density": 0.5,
        "initial_grass3_density": 0.8,
        "initial_herbivore1_density": 0.1,
        "initial_herbivore2_density": 0.3,
        "initial_herbivore3_density": 0.6,
        "initial_carnivore1_density": 0.1,
        "initial_carnivore2_density": 0.2,
        "initial_carnivore3_density": 0.3,
        "herbivore1_max_hunger": 10,
        "herbivore2_max_hunger": 15,
        "herbivore3_max_hunger": 20,
        "carnivore1_max_hunger": 2,
        "carnivore2_max_hunger": 3,
        "carnivore3_max_hunger": 4,
        "disaster_duration": 5,
        "disaster_probability": 0.01,
    }
    return params

params = set_parameters()

grid_size = params["grid_size"]
steps = params["steps"]
initial_grass1_density = params["initial_grass1_density"]
initial_grass2_density = params["initial_grass2_density"]
initial_grass3_density = params["initial_grass3_density"]

initial_herbivore1_density = params["initial_herbivore1_density"]
initial_herbivore2_density = params["initial_herbivore2_density"]
initial_herbivore3_density = params["initial_herbivore3_density"]

initial_carnivore1_density = params["initial_carnivore1_density"]
initial_carnivore2_density = params["initial_carnivore2_density"]
initial_carnivore3_density = params["initial_carnivore3_density"]

herbivore1_max_hunger = params["herbivore1_max_hunger"]
herbivore2_max_hunger = params["herbivore2_max_hunger"]
herbivore3_max_hunger = params["herbivore3_max_hunger"]

carnivore1_max_hunger = params["carnivore1_max_hunger"]
carnivore2_max_hunger = params["carnivore2_max_hunger"]
carnivore3_max_hunger = params["carnivore3_max_hunger"]

disaster_duration = params["disaster_duration"]
disaster_probability = params["disaster_probability"]
```
Function set_parameters():
    Define all parameters (grid size, initial densities, hunger limits, disaster settings)
    Return parameters as a dictionary

---
Create a 3D grid with 10 layers, where each layer represents:
    Layer 0-2: Grass types
    Layer 3-5: Herbivore types
    Layer 6-8: Carnivore types
    Layer 9: Unused (can be extended for other features)

Initialize grids for hunger tracking for herbivores and carnivores.
Randomly populate the grid based on initial densities.

```python
def count_neighbors(grid, x, y, layer):
    count = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i == x and j == y) or i < 0 or j < 0 or i >= grid_size or j >= grid_size:
                continue
            if grid[i, j, layer] == 1:
                count += 1
    return count
```

Function count_neighbors(grid, x, y, layer):
    Count the number of neighboring cells in a specific layer that are occupied.
    Skip out-of-bound cells and the current cell itself.
    Return the count of neighbors.

Function random_move(grid, x, y, layer):
    Randomly choose a direction (up, down, left, right).
    Check if the new position is empty (no same type or grass).
    Move the entity to the new position.
    Return the new coordinates.

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

Create animation using FuncAnimation:
    - Loop through `steps` number of frames.
    - Update the grid and visualization at each frame.
Show the animation.
