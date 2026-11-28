import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# --- 1. Simulation Parameters ---
ROAD_LENGTH = 120     # Number of cells on a circular highway
NUM_CARS = 35         # Total vehicles on the road
V_MAX = 5             # Maximum speed (cells per step)
P_SLOW = 0.25         # Probability a driver randomly slows down
STEPS = 100           # Number of time steps to simulate
NUM_WORKERS = 4       # Number of parallel threads

# --- 2. Initialize Road Grid ---
# -1 = empty cell, 0..V_MAX = car present with that speed
road = np.full(ROAD_LENGTH, -1, dtype=int)
car_positions = np.random.choice(ROAD_LENGTH, size=NUM_CARS, replace=False)
road[car_positions] = np.random.randint(0, V_MAX + 1, size=NUM_CARS)


# --- 3. Parallel Cellular Update Function ---
def update_chunk(args):
    """Applies Nagel-Schreckenberg local rules to a slice of the road."""
    current_road, start_idx, end_idx = args
    n = len(current_road)
    chunk_updates = []

    for i in range(start_idx, end_idx):
        v = current_road[i]
        if v == -1:
            continue  # Empty cell

        # Rule 1: Accelerate
        v = min(v + 1, V_MAX)

        # Rule 2: Brake to avoid hitting the car ahead
        gap = 0
        while gap < v and current_road[(i + gap + 1) % n] == -1:
            gap += 1
        v = min(v, gap)

        # Rule 3: Randomization (driver hesitation)
        if v > 0 and np.random.rand() < P_SLOW:
            v -= 1

        # Store new position and speed
        new_pos = (i + v) % n
        chunk_updates.append((new_pos, v))

    return chunk_updates


# --- 4. Run Parallel Simulation ---
history = np.zeros((STEPS, ROAD_LENGTH))
chunk_size = ROAD_LENGTH // NUM_WORKERS
chunks = [(i * chunk_size, (i + 1) * chunk_size if i < NUM_WORKERS - 1 else ROAD_LENGTH)
          for i in range(NUM_WORKERS)]

with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    for step in range(STEPS):
        # Record occupied cells (1 = car, 0 = empty) for plotting
        history[step] = (road >= 0).astype(int)

        # Process all road chunks in parallel
        tasks = [(road, start, end) for start, end in chunks]
        results = executor.map(update_chunk, tasks)

        # Build the next state from parallel results
        next_road = np.full(ROAD_LENGTH, -1, dtype=int)
        for chunk_updates in results:
            for pos, speed in chunk_updates:
                next_road[pos] = speed

        road = next_road


# --- 5. Visualize Traffic Flow (Space-Time Diagram) ---
plt.figure(figsize=(10, 6))
plt.imshow(history, cmap="binary", interpolation="nearest", aspect="auto")
plt.xlabel("Road Position (Cells)")
plt.ylabel("Time Step")
plt.title("Parallel Cellular Traffic Simulation (Black = Vehicle)")
plt.tight_layout()
plt.show()
