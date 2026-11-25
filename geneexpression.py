import random

POP_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1

# Plant growth prediction model
def predict_growth(individual):
    sunlight, water, temperature, nutrients = individual

    growth = (
        100
        - (sunlight - 8) ** 2
        - ((water - 500) / 100) ** 2
        - (temperature - 25) ** 2
        - (nutrients - 50) ** 2 / 100
    )

    return max(0, growth)

# Generate random plants
def create_population():
    population = []

    for _ in range(POP_SIZE):
        individual = [
            random.uniform(0, 12),     # Sunlight hours
            random.uniform(100, 1000), # Water in ml
            random.uniform(10, 40),    # Temperature
            random.uniform(0, 100)     # Nutrients
        ]

        population.append(individual)

    return population

# Tournament selection
def selection(population):
    candidates = random.sample(population, 3)
    return max(candidates, key=predict_growth)

# Crossover
def crossover(parent1, parent2):
    child = []

    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])

    return child

# Mutation
def mutation(individual):
    if random.random() < MUTATION_RATE:
        individual[0] += random.uniform(-1, 1)
        individual[1] += random.uniform(-50, 50)
        individual[2] += random.uniform(-2, 2)
        individual[3] += random.uniform(-10, 10)

    individual[0] = max(0, min(12, individual[0]))
    individual[1] = max(100, min(1000, individual[1]))
    individual[2] = max(10, min(40, individual[2]))
    individual[3] = max(0, min(100, individual[3]))

    return individual

# Genetic algorithm
def genetic_algorithm():
    population = create_population()

    for generation in range(GENERATIONS):
        new_population = []

        # Elitism: preserve the best individual
        best = max(population, key=predict_growth)
        new_population.append(best.copy())

        while len(new_population) < POP_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)
            child = mutation(child)

            new_population.append(child)

        population = new_population

        best = max(population, key=predict_growth)

        print("Generation:", generation + 1,
              "Growth Score:", round(predict_growth(best), 2))

    best = max(population, key=predict_growth)

    print("\n===== OPTIMAL PLANT GROWTH CONDITIONS =====")
    print("Sunlight:", round(best[0], 2), "hours")
    print("Water:", round(best[1], 2), "ml")
    print("Temperature:", round(best[2], 2), "°C")
    print("Nutrients:", round(best[3], 2))
    print("Predicted Growth Score:", round(predict_growth(best), 2))

genetic_algorithm()
