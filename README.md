This program creates an experimental environment for ecosystems, allowing for easy modification of initial populations, characteristics of organisms, and environmental conditions.  
The main features include:
1. **Initial Setup**
2. **Counting Surrounding Organisms**
3. **Random Movement**
4. **Organism Behavior Rules**
5. **Real-time Animation and Population Tracking**

---

### **1. Initial Setup**  
In the initial setup, it defines key parameters such as: grid size (the size of the area/environment where each organism resides), the number of steps (the number of actions organisms take), the initial populations of plants, herbivores, and carnivores, the hunger period for each, and the probability of disasters.

For Example:
```python
def set_parameters():
    params = {
        "grid_size": 100,                # Grid size: 100x100 cells
        "steps": 200,                    # Total simulation steps
        "initial_grass1_density": 0.2,   # Initial density of Grass1
        "initial_grass2_density": 0.5,   # Initial density of Grass2
        "initial_grass3_density": 0.8,   # Initial density of Grass3
        "initial_herbivore1_density": 0.1, # Herbivore1 density
        "initial_herbivore2_density": 0.3, # Herbivore2 density
        "initial_herbivore3_density": 0.6, # Herbivore3 density
        "initial_carnivore1_density": 0.1, # Carnivore1 density
        "initial_carnivore2_density": 0.2, # Carnivore2 density
        "initial_carnivore3_density": 0.3, # Carnivore3 density
        "herbivore1_max_hunger": 10,     # Hunger threshold for Herbivore1
        "herbivore2_max_hunger": 15,     # Hunger threshold for Herbivore2
        "herbivore3_max_hunger": 20,     # Hunger threshold for Herbivore3
        "carnivore1_max_hunger": 2,      # Hunger threshold for Carnivore1
        "carnivore2_max_hunger": 3,      # Hunger threshold for Carnivore2
        "carnivore3_max_hunger": 4,      # Hunger threshold for Carnivore3
        "disaster_duration": 5,          # Duration of disasters
        "disaster_probability": 0.01,    # Probability of disasters per step
    }
    return params
```

##**Grid Initialization**  
For example:  
```python
grid[:, :, 0] = np.random.choice(
    [0, 1], p=[1 - initial_grass1_density, initial_grass1_density], size=(grid_size, grid_size)
)
```
This algorithm creates layers within the grid, placing "plants (1)" in the 0th layer.  
- `{0, 1}` indicates whether a plant is absent (0) or present (1).  
- `p` represents the probability distribution of 0 and 1 for "plants (1), based on the defined parameters".  
- `size` specifies the range where "plants (1)" are arranged (Grid Dimension).  

In this way, the grid is divided into nine layers, and organisms are placed in each layer:
Layer 0-2 : Grass
Layer 3-5 : Herbivores
Layer 6-8 : Carnivores

---

### **2. Counting Surrounding Organisms**  
This step counts the number of organisms around a target organism, placed at the center (e.g., at `(0, 0)`).  
Using a **`for` loop**, the algorithm calculates the total number of organisms within the range `(x-1, x, x+1)` and `(y-1, y, y+1)` (a 3x3 grid).  

The center organism `(0, 0)` and positions outside the grid boundaries are excluded from the count:
```python
if (i == x and j == y) or i < 0 or j < 0 or i >= grid_size or j >= grid_size:
    continue
```

---

### **3. Random Movement**  
Organisms can move randomly in one of four directions: up, down, left, or right, centered on `(0, 0)`.  
```python
move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
np.random.shuffle(move_directions)
```
This shuffles the movement directions randomly.

The new position `(new_x, new_y)` is set as follows:  
- If the target position is occupied by another organism, the movement fails.  
- If the position is empty, the organism moves.

```python
for move in move_directions:
    new_x = (x + move[0]) % grid_size
    new_y = (y + move[1]) % grid_size
   
    if grid[new_x, new_y, layer] == 0 and grid[new_x, new_y, 0] == 0:
        grid[new_x, new_y, layer] = 1
        grid[x, y, layer] = 0
        return new_x, new_y 
return x, y 
```

---

### **4. Organism Behavior Rules**  
Reproduction, starvation, and predation are defined using the organism count logic.  
By using a **`for` loop**, the rules are applied to all organisms in the grid.

---

### **5. Animation**  
Using `cmap = mcolors.ListedColormap(...)`, colors are assigned to each type of organism when visualized on a graph.  

The program supports dual animations with this setup:
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
```

#### Data Tracking
To graph the population counts over time, the following lists are initialized to store organism counts:
```python
plant1_counts, plant2_counts, plant3_counts, herbivore1_counts, herbivore2_counts, herbivore3_counts, carnivore1_counts, carnivore2_counts, carnivore3_counts = [], [], [], [], [], [], [], [], []
```

#### Visualization of Movement (ax1)  
The `draw(grid)` function visualizes the movement of organisms within the grid.  
Organisms in the 9th layer (`grid[:, :, 8]`) represent the most predatory carnivores, while the 0th layer (`grid[:, :, 0]`) represents the first layer of plants.  

```python
def draw(grid):
    display_grid = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j, 8] == 1:  # Carnivore3
                display_grid[i, j] = 9
            elif grid[i, j, 7] == 1:  # Carnivore2
                display_grid[i, j] = 8
            elif grid[i, j, 6] == 1:  # Carnivore1
                display_grid[i, j] = 7
            ...
    ax1.imshow(display_grid, cmap=cmap, vmin=0, vmax=9)
    ax1.set_title("Ecosystem Simulation")
```

#### Population Tracking (ax2)  
The `plant1_counts` list is updated using the `append` method:  
```python
plant1_counts.append(np.sum(grid[:, :, 0]))
```
This appends the total count of "plants (1)" in `grid[:, :, 0]` at each step to the list, enabling the visualization of population changes over time.

---

### **Summary**
This algorithm leverages the `append` method to record the total number of "plants (1)" in `plant1_counts` at each step, enabling the graph (ax2) to visualize population trends. Meanwhile, the movement of organisms within the grid is animated in real time in ax1.
