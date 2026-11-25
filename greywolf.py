import random

def fitness(x):
    return -x**2 + 10*x + 5

def gwo():
    n = 10
    iterations = 50

    wolves = [random.uniform(-10, 10) for _ in range(n)]

    print("Initial Wolves:", wolves)

    for t in range(iterations):
        wolves.sort(key=fitness, reverse=True)

        alpha = wolves[0]
        beta = wolves[1]
        delta = wolves[2]

        a = 2 - (2 * t / iterations)

        new_wolves = []

        for x in wolves:
            r1 = random.random()
            r2 = random.random()
            A1 = 2*a*r1 - a
            C1 = 2*r2
            D1 = abs(C1*alpha - x)
            X1 = alpha - A1*D1

            r1 = random.random()
            r2 = random.random()
            A2 = 2*a*r1 - a
            C2 = 2*r2
            D2 = abs(C2*beta - x)
            X2 = beta - A2*D2

            r1 = random.random()
            r2 = random.random()
            A3 = 2*a*r1 - a
            C3 = 2*r2
            D3 = abs(C3*delta - x)
            X3 = delta - A3*D3

            new_x = (X1 + X2 + X3) / 3
            new_wolves.append(new_x)

        wolves = new_wolves

        best = max(wolves, key=fitness)

        print("Iteration:", t+1,
              "Best X:", round(best, 4),
              "Fitness:", round(fitness(best), 4))

    best = max(wolves, key=fitness)

    print("\nOptimal Solution:", round(best, 4))
    print("Maximum Fitness:", round(fitness(best), 4))

gwo()
