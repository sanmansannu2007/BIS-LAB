import random

def fitness(x):
    return -(x[0]-30)**2 - (x[1]-20)**2 - (x[2]-25)**2 - (x[3]-25)**2

def pso():
    n = 10
    iterations = 50
    w = 0.5
    c1 = 1.5
    c2 = 1.5

    particles = [[random.uniform(0,100) for _ in range(4)] for _ in range(n)]
    velocity = [[0 for _ in range(4)] for _ in range(n)]

    pbest = particles.copy()
    gbest = max(pbest, key=fitness)

    for t in range(iterations):
        for i in range(n):
            for j in range(4):
                r1 = random.random()
                r2 = random.random()

                velocity[i][j] = (
                    w * velocity[i][j]
                    + c1 * r1 * (pbest[i][j] - particles[i][j])
                    + c2 * r2 * (gbest[j] - particles[i][j])
                )

                particles[i][j] += velocity[i][j]
                particles[i][j] = max(0, min(100, particles[i][j]))

            for i in range(n):
                if fitness(particles[i]) > fitness(pbest[i]):
                    pbest[i] = particles[i].copy()

            gbest = max(pbest, key=fitness)

        print("Iteration:", t+1, "Best Fitness:", round(fitness(gbest), 4))

    print("\nOptimal Smart City Allocation")
    print("Roads:", round(gbest[0], 2), "%")
    print("Hospitals:", round(gbest[1], 2), "%")
    print("Parks:", round(gbest[2], 2), "%")
    print("Housing:", round(gbest[3], 2), "%")

pso()
