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
```python
grid = np.zeros((grid_size, grid_size, 10), dtype=int)
herbivore1_hunger = np.zeros((grid_size, grid_size), dtype=int)
herbivore2_hunger = np.zeros((grid_size, grid_size), dtype=int)
herbivore3_hunger = np.zeros((grid_size, grid_size), dtype=int)
carnivore1_hunger = np.zeros((grid_size, grid_size), dtype=int)
carnivore2_hunger = np.zeros((grid_size, grid_size), dtype=int)
carnivore3_hunger = np.zeros((grid_size, grid_size), dtype=int)
disaster_counter = 0

grid[:, :, 0] = np.random.choice(
    [0, 1], p=[1 - initial_grass1_density, initial_grass1_density], size=(grid_size, grid_size)
)
grid[:, :, 1] = np.random.choice(
    [0, 1], p=[1 - initial_grass2_density, initial_grass2_density], size=(grid_size, grid_size)
)
grid[:, :, 2] = np.random.choice(
    [0, 1], p=[1 - initial_grass3_density, initial_grass3_density], size=(grid_size, grid_size)
)

grid[:, :, 3] = np.random.choice(
    [0, 1], p=[1 - initial_herbivore1_density, initial_herbivore1_density], size=(grid_size, grid_size)
)
grid[:, :, 4] = np.random.choice(
    [0, 1], p=[1 - initial_herbivore2_density, initial_herbivore2_density], size=(grid_size, grid_size)
)
grid[:, :, 5] = np.random.choice(
    [0, 1], p=[1 - initial_herbivore3_density, initial_herbivore3_density], size=(grid_size, grid_size)
)

grid[:, :, 6] = np.random.choice(
    [0, 1], p=[1 - initial_carnivore1_density, initial_carnivore1_density], size=(grid_size, grid_size)
)
grid[:, :, 7] = np.random.choice(
    [0, 1], p=[1 - initial_carnivore2_density, initial_carnivore2_density], size=(grid_size, grid_size)
)
grid[:, :, 8] = np.random.choice(
    [0, 1], p=[1 - initial_carnivore3_density, initial_carnivore3_density], size=(grid_size, grid_size)
)
```
Create a 3D grid with 10 layers, where each layer represents:
    Layer 0-2: Grass types
    Layer 3-5: Herbivore types
    Layer 6-8: Carnivore types
    Layer 9: Unused (can be extended for other features)

Initialize grids for hunger tracking for herbivores and carnivores.
Randomly populate the grid based on initial densities.

---
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

---
```python
def random_move(grid, x, y, layer):
    move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    np.random.shuffle(move_directions)

    for move in move_directions:
        new_x = (x + move[0]) % grid_size
        new_y = (y + move[1]) % grid_size

        if grid[new_x, new_y, layer] == 0 and grid[new_x, new_y, 0] == 0:
            grid[new_x, new_y, layer] = 1
            grid[x, y, layer] = 0
            return new_x, new_y
    return x, y
```
Function random_move(grid, x, y, layer):
    Randomly choose a direction (up, down, left, right).
    Check if the new position is empty (no same type or grass).
    Move the entity to the new position.
    Return the new coordinates.

---
```python
def update(grid, herbivore1_hunger, herbivore2_hunger, herbivore3_hunger, carnivore1_hunger, carnivore2_hunger, carnivore3_hunger, disaster_counter):
    new_grid = grid.copy()
    new_herbivore1_hunger = herbivore1_hunger.copy()
    new_herbivore2_hunger = herbivore2_hunger.copy()
    new_herbivore3_hunger = herbivore3_hunger.copy()

    new_carnivore1_hunger = carnivore1_hunger.copy()
    new_carnivore2_hunger = carnivore2_hunger.copy()
    new_carnivore3_hunger = carnivore3_hunger.copy()

    if np.random.rand() < disaster_probability:
        disaster_counter = disaster_duration

    if disaster_counter > 0:
        disaster_counter -= 1
```
Function update(grid, hunger_grids, disaster_counter):
    If a random disaster occurs:
        Set disaster_counter to its duration.

---
```python
    for i in range(grid_size):
        for j in range(grid_size):
            # Grass1
            if grid[i, j, 0] == 1:
                if count_neighbors(grid, i, j, 3) >= 3 or count_neighbors(grid, i, j, 4) >= 3 or count_neighbors(grid, i, j, 5) >= 3:
                    new_grid[i, j, 0] = 0
                elif count_neighbors(grid, i, j, 0) >= 3 and disaster_counter == 0:
                    new_grid[i, j, 0] = 1
            elif grid[i, j, 0] == 0:
                if count_neighbors(grid, i, j, 0) == 3 and disaster_counter == 0:
                    new_grid[i, j, 0] = 1

            # Grass2
            if grid[i, j, 1] == 1:
                if count_neighbors(grid, i, j, 3) >= 3 or count_neighbors(grid, i, j, 4) >= 3 or count_neighbors(grid, i, j, 5) >= 3:
                    new_grid[i, j, 1] = 0
                elif count_neighbors(grid, i, j, 1) >= 3 and disaster_counter == 0:
                    new_grid[i, j, 1] = 1
            elif grid[i, j, 1] == 0:
                if count_neighbors(grid, i, j, 1) == 3 and disaster_counter == 0:
                    new_grid[i, j, 1] = 1

            # Grass3
            if grid[i, j, 2] == 1:
                if count_neighbors(grid, i, j, 3) >= 3 or count_neighbors(grid, i, j, 4) >= 3 or count_neighbors(grid, i, j, 5) >= 3:
                    new_grid[i, j, 2] = 0
                elif count_neighbors(grid, i, j, 2) >= 3 and disaster_counter == 0:
                    new_grid[i, j, 2] = 1
            elif grid[i, j, 2] == 0:
                if count_neighbors(grid, i, j, 2) == 3 and disaster_counter == 0:
                    new_grid[i, j, 2] = 1

            # Herbivore1
            if grid[i, j, 3] == 1:
                i, j = random_move(new_grid, i, j, 3)

                if count_neighbors(new_grid, i, j, 0) >= 1 or count_neighbors(new_grid, i, j, 1) >= 1 or count_neighbors(new_grid, i, j, 2) >= 1:
                    new_grid[i, j, 3] = 1
                    new_herbivore1_hunger[i, j] = 0
                else:
                    new_herbivore1_hunger[i, j] += 1
                    if new_herbivore1_hunger[i, j] >= herbivore1_max_hunger:
                        new_grid[i, j, 3] = 0

                if count_neighbors(new_grid, i, j, 3) > 3:
                    new_grid[i, j, 3] = 0
                if count_neighbors(new_grid, i, j, 3) < 2:
                    new_grid[i, j, 3] = 0
                if count_neighbors(new_grid, i, j, 3) == 2 or count_neighbors(new_grid, i, j, 3) == 3:
                    new_grid[i, j, 3] = 1
            elif grid[i, j, 3] == 0:
                if grid[i, j, 0] == 1:
                    if count_neighbors(grid, i, j, 3) == 2 or count_neighbors(grid, i, j, 3) == 3:
                        new_grid[i, j, 3] = 1

            # Herbivore2
            if grid[i, j, 4] == 1:
                i, j = random_move(new_grid, i, j, 4)

                if count_neighbors(new_grid, i, j, 0) >= 1 or count_neighbors(new_grid, i, j, 1) >= 1 or count_neighbors(new_grid, i, j, 2) >= 1:
                    new_grid[i, j, 4] = 1
                    new_herbivore2_hunger[i, j] = 0
                else:
                    new_herbivore2_hunger[i, j] += 1
                    if new_herbivore2_hunger[i, j] >= herbivore2_max_hunger:
                        new_grid[i, j, 4] = 0
                if count_neighbors(new_grid, i, j, 4) > 3:
                    new_grid[i, j, 4] = 0
                if count_neighbors(new_grid, i, j, 4) < 2:
                    new_grid[i, j, 4] = 0
                if count_neighbors(new_grid, i, j, 4) == 2 or count_neighbors(new_grid, i, j, 4) == 3:
                    new_grid[i, j, 4] = 1
            elif grid[i, j, 4] == 0:
                if grid[i, j, 1] == 1:
                    if count_neighbors(grid, i, j, 4) == 2 or count_neighbors(grid, i, j, 4) == 3:
                        new_grid[i, j, 4] = 1

            # Herbivore3
            if grid[i, j, 5] == 1:
                i, j = random_move(new_grid, i, j, 5)

                if count_neighbors(new_grid, i, j, 0) >= 1 or count_neighbors(new_grid, i, j, 1) >= 1 or count_neighbors(new_grid, i, j, 2) >= 1:
                    new_grid[i, j, 5] = 1
                    new_herbivore3_hunger[i, j] = 0
                else:
                    new_herbivore3_hunger[i, j] += 1
                    if new_herbivore3_hunger[i, j] >= herbivore3_max_hunger:
                        new_grid[i, j, 5] = 0
                if count_neighbors(new_grid, i, j, 5) > 3:
                    new_grid[i, j, 5] = 0
                if count_neighbors(new_grid, i, j, 5) < 2:
                    new_grid[i, j, 5] = 0
                if count_neighbors(new_grid, i, j, 5) == 2 or count_neighbors(new_grid, i, j, 5) == 3:
                    new_grid[i, j, 5] = 1
            elif grid[i, j, 5] == 0:
                if grid[i, j, 2] == 1:
                    if count_neighbors(grid, i, j, 5) == 2 or count_neighbors(grid, i, j, 5) == 3:
                        new_grid[i, j, 5] = 1

            # Carnivore1
            if grid[i, j, 6] == 1:
                i, j = random_move(new_grid, i, j, 6)

                if count_neighbors(new_grid, i, j, 3) >= 1 or count_neighbors(new_grid, i, j, 4) >= 1 or count_neighbors(new_grid, i, j, 5) >= 1:
                    new_grid[i, j, 6] = 1
                    new_carnivore1_hunger[i, j] = 0
                else:
                    new_carnivore1_hunger[i, j] += 1
                    if new_carnivore1_hunger[i, j] >= carnivore1_max_hunger:
                        new_grid[i, j, 6] = 0
                if count_neighbors(new_grid, i, j, 6) > 3:
                    new_grid[i, j, 6] = 0
                if count_neighbors(new_grid, i, j, 6) == 3:
                    new_grid[i, j, 6] = 1
            elif grid[i, j, 6] == 0:
                if grid[i, j, 3] == 1:
                    if count_neighbors(grid, i, j, 6) == 2 or count_neighbors(grid, i, j, 6) == 3:
                        new_grid[i, j, 6] = 1

            # Carnivore2
            if grid[i, j, 7] == 1:
                i, j = random_move(new_grid, i, j, 7)

                if count_neighbors(new_grid, i, j, 3) >= 1 or count_neighbors(new_grid, i, j, 4) >= 1 or count_neighbors(new_grid, i, j, 5) >= 1:
                    new_grid[i, j, 7] = 1
                    new_carnivore2_hunger[i, j] = 0
                else:
                    new_carnivore2_hunger[i, j] += 1
                    if new_carnivore2_hunger[i, j] >= carnivore2_max_hunger:
                        new_grid[i, j, 7] = 0
                if count_neighbors(new_grid, i, j, 7) > 3:
                    new_grid[i, j, 7] = 0
                if count_neighbors(new_grid, i, j, 7) == 3:
                    new_grid[i, j, 7] = 1
            elif grid[i, j, 7] == 0:
                if grid[i, j, 4] == 1:
                    if count_neighbors(grid, i, j, 7) == 2 or count_neighbors(grid, i, j, 7) == 3:
                        new_grid[i, j, 7] = 1

            # Carnivore3
            if grid[i, j, 8] == 1:
                i, j = random_move(new_grid, i, j, 8)

                if count_neighbors(new_grid, i, j, 3) >= 1 or count_neighbors(new_grid, i, j, 4) >= 1 or count_neighbors(new_grid, i, j, 5) >= 1:
                    new_grid[i, j, 8] = 1
                    new_carnivore3_hunger[i, j] = 0
                else:
                    new_carnivore3_hunger[i, j] += 1
                    if new_carnivore3_hunger[i, j] >= carnivore3_max_hunger:
                        new_grid[i, j, 8] = 0
                if count_neighbors(new_grid, i, j, 8) > 3:
                    new_grid[i, j, 8] = 0
                if count_neighbors(new_grid, i, j, 8) == 3:
                    new_grid[i, j, 8] = 1
            elif grid[i, j, 8] == 0:
                if grid[i, j, 5] == 1:
                    if count_neighbors(grid, i, j, 8) == 2 or count_neighbors(grid, i, j, 8) == 3:
                        new_grid[i, j, 8] = 1


    return new_grid, new_herbivore1_hunger, new_carnivore1_hunger, new_herbivore2_hunger, new_carnivore2_hunger, new_herbivore3_hunger, new_carnivore3_hunger, disaster_counter
```
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
```python
cmap = mcolors.ListedColormap(['white', 'yellow','green','blue', 'purple','orange','pink', 'red', 'cyan', 'brown'])

# Visualization settings with dual plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Initialize data tracking
plant1_counts, plant2_counts, plant3_counts, herbivore1_counts, herbivore2_counts, herbivore3_counts, carnivore1_counts, carnivore2_counts, carnivore3_counts = [], [], [], [], [], [], [], [], []

def draw(grid):
    display_grid = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j, 8] == 1:  # Carnivore3
                display_grid[i, j] = 9
            elif grid[i, j, 7] == 1:  # Carnivore2
                display_grid[i, j] = 8
            elif grid[i, j, 6] == 1:  # Carnivore1
                display_grid[i, j] = 7
            elif grid[i, j, 5] == 1:  # Herbivore3
                display_grid[i, j] = 6
            elif grid[i, j, 4] == 1:  # Herbivore2
                display_grid[i, j] = 5
            elif grid[i, j, 3] == 1:  # Herbivore1
                display_grid[i, j] = 4
            elif grid[i, j, 2] == 1:  # Grass3
                display_grid[i, j] = 3
            elif grid[i, j, 1] == 1:  # Grass2
                display_grid[i, j] = 2
            elif grid[i, j, 0] == 1:  # Grass1
                display_grid[i, j] = 1

    ax1.imshow(display_grid, cmap=cmap, vmin=0, vmax=9)
    ax1.set_title("Ecosystem Simulation")
```
Function draw(grid):
    Convert 3D grid into a 2D display grid with values:
        1: Grass1, 2: Grass2, 3: Grass3
        4-6: Herbivores, 7-9: Carnivores
    Display the grid using a custom color map.

```python
def animate(frame):
    global grid, herbivore1_hunger, carnivore1_hunger, herbivore2_hunger, carnivore2_hunger, herbivore3_hunger, carnivore3_hunger, disaster_counter
    grid, herbivore1_hunger, carnivore1_hunger, herbivore2_hunger, carnivore2_hunger, herbivore3_hunger, carnivore3_hunger, disaster_counter = update(grid, herbivore1_hunger, carnivore1_hunger, herbivore2_hunger, carnivore2_hunger, herbivore3_hunger, carnivore3_hunger, disaster_counter)

    # Track population counts
    plant1_counts.append(np.sum(grid[:, :, 0]))
    plant2_counts.append(np.sum(grid[:, :, 1]))
    plant3_counts.append(np.sum(grid[:, :, 2]))
    herbivore1_counts.append(np.sum(grid[:, :, 3]))
    herbivore2_counts.append(np.sum(grid[:, :, 4]))
    herbivore3_counts.append(np.sum(grid[:, :, 5]))
    carnivore1_counts.append(np.sum(grid[:, :, 6]))
    carnivore2_counts.append(np.sum(grid[:, :, 7]))
    carnivore3_counts.append(np.sum(grid[:, :, 8]))

    # Update ecosystem display
    ax1.clear()
    draw(grid)

    # Update population graph
    ax2.clear()
    ax2.plot(plant1_counts, label="Grass1", color="yellow")
    ax2.plot(plant2_counts, label="Grass2", color="green")
    ax2.plot(plant3_counts, label="Grass3", color="blue")

    ax2.plot(herbivore1_counts, label="Herbivores1", color="purple")
    ax2.plot(herbivore2_counts, label="Herbivores2", color="orange")
    ax2.plot(herbivore3_counts, label="Herbivores3", color="pink")

    ax2.plot(carnivore1_counts, label="Carnivores1", color="red")
    ax2.plot(carnivore2_counts, label="Carnivores2", color="cyan")
    ax2.plot(carnivore3_counts, label="Carnivores3", color="brown")
    ax2.legend()
    ax2.set_title("Population Over Time")
    ax2.set_xlabel("Steps")
    ax2.set_ylabel("Population")
```
Function animate(frame):
    Call the update function to process one simulation step.
    Track population counts for plants, herbivores, and carnivores.
    Update two plots:
        - Left: Grid visualization
        - Right: Population trends over time

---
```python
# Execute animation
ani = animation.FuncAnimation(fig, animate, frames=steps, interval=200)
plt.show()
```
Create animation using FuncAnimation:
    - Loop through `steps` number of frames.
    - Update the grid and visualization at each frame.
Show the animation.
