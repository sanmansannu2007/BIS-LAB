import random

graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5, 'E': 7},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'F': 6},
    'E': {'B': 7, 'C': 10, 'D': 2, 'F': 3},
    'F': {'D': 6, 'E': 3}
}

def aco(start, end, ants=10, iterations=20):
    alpha = 1
    beta = 2
    evaporation = 0.5
    Q = 100

    pheromone = {}

    for node in graph:
        for neighbor in graph[node]:
            pheromone[(node, neighbor)] = 1.0

    best_path = None
    best_cost = float('inf')

    for iteration in range(iterations):
        all_paths = []

        for ant in range(ants):
            path = [start]
            current = start

            while current != end:
                neighbors = [
                    n for n in graph[current]
                    if n not in path
                ]

                if not neighbors:
                    break

                probabilities = []

                for neighbor in neighbors:
                    tau = pheromone[(current, neighbor)] ** alpha
                    eta = (1 / graph[current][neighbor]) ** beta
                    probabilities.append(tau * eta)

                total = sum(probabilities)

                probabilities = [
                    p / total for p in probabilities
                ]

                next_node = random.choices(
                    neighbors, weights=probabilities
                )[0]

                path.append(next_node)
                current = next_node

            if current == end:
                cost = 0

                for i in range(len(path) - 1):
                    cost += graph[path[i]][path[i + 1]]

                all_paths.append((path, cost))

                if cost < best_cost:
                    best_cost = cost
                    best_path = path.copy()

        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation)

        for path, cost in all_paths:
            deposit = Q / cost

            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1])
                pheromone[edge] += deposit

                reverse_edge = (path[i + 1], path[i])
                pheromone[reverse_edge] += deposit

        if all_paths:
            iteration_best = min(all_paths, key=lambda x: x[1])

            print("Iteration:", iteration + 1)
            print("Best Path:", iteration_best[0])
            print("Path Cost:", iteration_best[1])
            print("Global Best Cost:", best_cost)
            print()

    print("========== FINAL RESULT ==========")
    print("Optimal Path:", best_path)
    print("Minimum Cost:", best_cost)

aco('A', 'F')
