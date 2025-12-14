import numpy as np

def fitness(position):
    x, y = position
    return x**2 + y**2 - 4*x - 6*y

num_particles = 3
num_iterations = 10
w = 0.5
c1 = 1.5
c2 = 2
r1 = 0.5
r2 = 0.3
dim = 2

positions = np.array([
    [1.0, 1.0],
    [5.0, 2.0],
    [0.0, 4.0]
])

velocities = np.zeros((num_particles, dim))

pbest_positions = positions.copy()
pbest_values = np.array([fitness(p) for p in positions])

gbest_index = np.argmin(pbest_values)
gbest_position = pbest_positions[gbest_index].copy()
gbest_value = pbest_values[gbest_index]

for iteration in range(num_iterations):
    print(f"\nIteration {iteration + 1}")

    for i in range(num_particles):
        velocities[i] = (
            w * velocities[i]
            + c1 * r1 * (pbest_positions[i] - positions[i])
            + c2 * r2 * (gbest_position - positions[i])
        )

        positions[i] = positions[i] + velocities[i]

        current_value = fitness(positions[i])

        if current_value < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = current_value

    gbest_index = np.argmin(pbest_values)
    gbest_position = pbest_positions[gbest_index].copy()
    gbest_value = pbest_values[gbest_index]

    print("Global Best Position:", gbest_position)
    print("Global Best Value:", gbest_value)

print("\nFinal Result")
print("Best Position Found:", gbest_position)
print("Minimum Function Value:", gbest_value)