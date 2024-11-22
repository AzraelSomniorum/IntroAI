import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
this is a test
# Set grid size, number of steps, and initial densities
grid_size = 50
steps = 100
initial_grass_density = 0.5  # Initial density of grass
initial_herbivore_density = 0.3  # Initial density of herbivores
initial_carnivore_density = 0.2  # Initial density of carnivores
herbivore_max_hunger = 15  # Number of steps before herbivores die from hunger
carnivore_max_hunger = 3  # Number of steps before carnivores die from hunger
disaster_duration = 5
disaster_probability = 0.01

# Grid representation where 0:empty, 1:grass, 2:herbivore, 3:carnivore
grid = np.zeros((grid_size, grid_size, 3), dtype=int)
herbivore_hunger = np.zeros((grid_size, grid_size), dtype=int)  # Hunger state of herbivores
carnivore_hunger = np.zeros((grid_size, grid_size), dtype=int)  # Hunger state of carnivores
disaster_counter = 0

# Randomly initialize grass, herbivores, and carnivores
grid[:, :, 0] = np.random.choice([0, 1], p=[1 - initial_grass_density, initial_grass_density], size=(grid_size, grid_size))  # Grass
grid[:, :, 1] = np.random.choice([0, 1], p=[1 - initial_herbivore_density, initial_herbivore_density], size=(grid_size, grid_size))  # Herbivores
grid[:, :, 2] = np.random.choice([0, 1], p=[1 - initial_carnivore_density, initial_carnivore_density], size=(grid_size, grid_size))  # Carnivores

# Neighbor count function
def count_neighbors(grid, x, y, layer):
    count = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i == x and j == y) or i < 0 or j < 0 or i >= grid_size or j >= grid_size:
                continue
            if grid[i, j, layer] == 1:
                count += 1
    return count

# Random movement for agents
def random_move(grid, x, y, layer):
    # Move randomly (up, down, left, right)
    move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    np.random.shuffle(move_directions)  # Shuffle movement directions randomly
    
    for move in move_directions:
        new_x = (x + move[0]) % grid_size
        new_y = (y + move[1]) % grid_size
        # If destination is empty, move
        if grid[new_x, new_y, layer] == 0 and grid[new_x, new_y, 0] == 0:
            grid[new_x, new_y, layer] = 1
            grid[x, y, layer] = 0
            return new_x, new_y  # Return new coordinates
    return x, y  # If movement is not possible, return original coordinates

# Update function for simulation
def update(grid, herbivore_hunger, carnivore_hunger, disaster_counter):
    new_grid = grid.copy()
    new_herbivore_hunger = herbivore_hunger.copy()
    new_carnivore_hunger = carnivore_hunger.copy()
    
    if np.random.rand() < disaster_probability:
        disaster_counter = disaster_duration
    
    if disaster_counter > 0:
        disaster_counter -= 1
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Rules for grass
            if grid[i, j, 0] == 1:  # If grass exists
                if count_neighbors(grid, i, j, 1) >= 3:  # Eaten by herbivores
                    new_grid[i, j, 0] = 0
                elif count_neighbors(grid, i, j, 0) >= 3 and disaster_counter == 0:  # Grass reproduces
                    new_grid[i, j, 0] = 1
            elif grid[i, j, 0] == 0:  # If no grass
                if count_neighbors(grid, i, j, 0) == 3 and disaster_counter == 0:  # Grass reproduces if exactly 3 grass neighbors
                    new_grid[i, j, 0] = 1

            # Rules for herbivores
            if grid[i, j, 1] == 1:  # If herbivore exists
                i, j = random_move(new_grid, i, j, 1)  # Move randomly
                
                if count_neighbors(new_grid, i, j, 0) >= 1:  # If there is grass, survive
                    new_grid[i, j, 1] = 1
                    new_herbivore_hunger[i, j] = 0  # Reset hunger state
                else:  # If no grass, hunger increases
                    new_herbivore_hunger[i, j] += 1
                    if new_herbivore_hunger[i, j] >= herbivore_max_hunger:  # Die from hunger
                        new_grid[i, j, 1] = 0
                if count_neighbors(new_grid, i, j, 1) > 3 or count_neighbors(new_grid, i, j, 1) < 2:
                    new_grid[i, j, 1] = 0
                if count_neighbors(new_grid, i, j, 1) == 3:
                    new_grid[i, j, 1] = 1
            elif grid[i, j, 1] == 0:  # If no herbivore
                if grid[i, j, 0] == 1:  # Reproduction condition
                    if count_neighbors(grid, i, j, 1) in [2, 3]:
                        new_grid[i, j, 1] = 1  # Reproduction

            # Rules for carnivores
            if grid[i, j, 2] == 1:  # If carnivore exists
                i, j = random_move(new_grid, i, j, 2)  # Move randomly
                
                if count_neighbors(new_grid, i, j, 1) >= 1:  # If herbivores are nearby, eat
                    new_grid[i, j, 2] = 1
                    new_carnivore_hunger[i, j] = 0  # Reset hunger state
                else:  # If no prey, hunger increases
                    new_carnivore_hunger[i, j] += 1
                    if new_carnivore_hunger[i, j] >= carnivore_max_hunger:  # Die from hunger
                        new_grid[i, j, 2] = 0
                if count_neighbors(new_grid, i, j, 2) > 3:
                    new_grid[i, j, 2] = 0
                if count_neighbors(new_grid, i, j, 2) == 3:
                    new_grid[i, j, 2] = 1
            elif grid[i, j, 2] == 0:
                if grid[i, j, 1] == 1:
                    if count_neighbors(grid, i, j, 2) in [2, 3]:
                        new_grid[i, j, 2] = 1

    return new_grid, new_herbivore_hunger, new_carnivore_hunger, disaster_counter

# Visualization settings
fig, ax = plt.subplots()
cmap = mcolors.ListedColormap(['white', 'green', 'blue', 'red'])

# Colormap
def draw(grid):
    display_grid = np.zeros((grid_size, grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j, 2] == 1:  # Carnivore
                display_grid[i, j] = 3
            elif grid[i, j, 1] == 1:  # Herbivore
                display_grid[i, j] = 2
            elif grid[i, j, 0] == 1:  # Grass
                display_grid[i, j] = 1
    
    ax.imshow(display_grid, cmap=cmap, vmin=0, vmax=3)

# Animation update function
def animate(step):
    global grid, herbivore_hunger, carnivore_hunger, disaster_counter
    grid, herbivore_hunger, carnivore_hunger, disaster_counter = update(grid, herbivore_hunger, carnivore_hunger, disaster_counter)
    ax.clear()
    draw(grid)

# Execute animation
ani = animation.FuncAnimation(fig, animate, frames=steps, interval=200)
plt.show()
