import random

def fitness(x):
    return -(x - 150) ** 2 + 1000

def cuckoo_search():
    n = 10
    iterations = 50
    pa = 0.25

    nests = [80, 120, 180, 200, 145, 90, 160, 130, 210, 150]

    print("Initial Nests:", nests)
    print("Initial Fitness:", [fitness(x) for x in nests])

    best = max(nests, key=fitness)

    for t in range(iterations):
        for i in range(n):
            new = nests[i] + random.uniform(-20, 20)
            new = max(0, min(255, new))

            j = random.randint(0, n - 1)

            if fitness(new) > fitness(nests[j]):
                nests[j] = new

        count = int(pa * n)

        for i in range(count):
            j = random.randint(0, n - 1)
            nests[j] = random.randint(0, 255)

        current = max(nests, key=fitness)

        if fitness(current) > fitness(best):
            best = current

        print("Iteration:", t + 1,
              "Best Threshold:", round(best, 2),
              "Fitness:", round(fitness(best), 2))

    threshold = round(best)

    print("\nOptimal Threshold:", threshold)
    print("Maximum Fitness:", round(fitness(best), 2))

    values = [40, 80, 120, 145, 150, 160, 180, 200, 220, 255]

    segmented = [1 if x > threshold else 0 for x in values]

    print("\nOriginal Values:", values)
    print("Segmented Values:", segmented)

cuckoo_search()
