import random
from concurrent.futures import ThreadPoolExecutor

# --- 1. Simulation Parameters ---
ROAD_LENGTH = 50      # Number of cells on the road
NUM_CARS = 18         # Total vehicles on the road
V_MAX = 5             # Maximum speed (cells per step)
P_SLOW = 0.25         # Probability a driver randomly slows down
STEPS = 15            # Number of time steps to display
NUM_WORKERS = 4       # Number of parallel threads

# --- 2. Initialize Road Grid ---
# -1 = empty cell, 0..V_MAX = car present with that speed
road = [-1] * ROAD_LENGTH
for pos in random.sample(range(ROAD_LENGTH), NUM_CARS):
    road[pos] = random.randint(0, V_MAX)


# --- 3. Parallel Cellular Update Function ---
def update_chunk(args):
    """Applies Nagel-Schreckenberg local rules to a slice of the road."""
    current_road, start_idx, end_idx = args
    n = len(current_road)
    chunk_updates = []

    for i in range(start_idx, end_idx):
        v = current_road[i]
        if v == -1:
            continue

        # Rule 1: Accelerate
        v = min(v + 1, V_MAX)

        # Rule 2: Brake to avoid hitting the car ahead
        gap = 0
        while gap < v and current_road[(i + gap + 1) % n] == -1:
            gap += 1
        v = min(v, gap)

        # Rule 3: Randomization (driver hesitation)
        if v > 0 and random.random() < P_SLOW:
            v -= 1

        new_pos = (i + v) % n
        chunk_updates.append((new_pos, v))

    return chunk_updates


def road_to_letters(current_road):
    """Converts road state to letters: F=Fast, M=Moving, S=Stopped, .=Empty."""
    symbols = []
    for cell in current_road:
        if cell == -1:
            symbols.append(".")
        elif cell == 0:
            symbols.append("S")   # Stopped (Jam)
        elif cell <= 3:
            symbols.append("M")   # Moving (Medium speed)
        else:
            symbols.append("F")   # Fast
    return "".join(symbols)


# --- 4. Run Parallel Simulation & Print Letter Output ---
chunk_size = ROAD_LENGTH // NUM_WORKERS
chunks = [
    (i * chunk_size, (i + 1) * chunk_size if i < NUM_WORKERS - 1 else ROAD_LENGTH)
    for i in range(NUM_WORKERS)
]

print("Legend: F = Fast Car | M = Moving Car | S = Stopped Car (Jam) | . = Empty Road\n")

with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    for step in range(STEPS):
        # Print current road state in letters
        line = road_to_letters(road)
        stopped = line.count("S")
        status = "CONGESTED" if stopped >= 5 else "MODERATE" if stopped >= 2 else "SMOOTH"
        print(f"Step {step:2d}: {line}  | Status: {status}")

        # Update all road chunks in parallel
        tasks = [(road, start, end) for start, end in chunks]
        results = executor.map(update_chunk, tasks)

        next_road = [-1] * ROAD_LENGTH
        for chunk_updates in results:
            for pos, speed in chunk_updates:
                next_road[pos] = speed
        road = next_road
