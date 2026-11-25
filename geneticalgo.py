import random

POP_SIZE = 10
GEN = 20
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 3

def fitness(x):
    return -(x*x) + 10*x + 5

def create_population():
    return [random.uniform(0, 10) for _ in range(POP_SIZE)]

def tournament_selection(population):
    selected = random.sample(population, TOURNAMENT_SIZE)
    winner = max(selected, key=fitness)
    return winner

def crossover(p1, p2):
    return (p1 + p2) / 2

def mutation(x):
    if random.random() < MUTATION_RATE:
        x += random.uniform(-1, 1)
    return max(0, min(10, x))

def genetic_algorithm():
    population = create_population()

    for generation in range(GEN):
        new_population = []

        for _ in range(POP_SIZE):
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            child = crossover(p1, p2)
            child = mutation(child)

            new_population.append(child)

        population = new_population

        best = max(population, key=fitness)

        print("Generation:", generation + 1,
              "Best solution:", round(best, 4),
              "Fitness:", round(fitness(best), 4))

    best_solution = max(population, key=fitness)

    print("\nBest solution:", round(best_solution, 4))
    print("Best fitness:", round(fitness(best_solution), 4))

genetic_algorithm()
