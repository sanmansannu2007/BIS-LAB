def initialize_cells():
    cells = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    return cells

def update_cells(cells):
    new_cells = []
    size = len(cells)

    for i in range(size):
        left = cells[i - 1]
        center = cells[i]
        right = cells[(i + 1) % size]

        if (left, center, right) in [(1, 1, 1), (1, 1, 0),
                                     (1, 0, 1), (1, 0, 0)]:
            new_cells.append(1)
        else:
            new_cells.append(0)

    return new_cells

def display_cells(cells, generation):
    print("Generation", generation, ":", end=" ")

    for cell in cells:
        if cell == 1:
            print("*", end=" ")
        else:
            print(".", end=" ")

    print()

def parallel_cellular_algorithm():
    generations = 10

    cells = initialize_cells()

    print("Cellular Automata using Parallel Cellular Algorithm")
    print("-----------------------------------------------")
    print("Initial Input:")
    display_cells(cells, 0)

    for generation in range(1, generations + 1):
        cells = update_cells(cells)
        display_cells(cells, generation)

parallel_cellular_algorithm()
