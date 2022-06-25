# https://developers.google.com/optimization/assignment/assignment_example

# Problem: Assign works at most one task, with no two workers performing the same task,
# while minimizing the total cost using the MIP solver

from ortools.linear_solver import pywraplp

# Rows represent how much it costs for a worker to do each task
costs = [
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100],
]
num_workers = len(costs)
num_tasks = len(costs[0])

# Create the mip solver with the SCIP backend
solver = pywraplp.Solver.CreateSolver('SCIP')

# x[i,j] is an array of 0-1 variables which will be 1 if worker i is assigned to task j
x = {}
for i in range(num_workers):
    for j in range(num_tasks):
        x[i, j] = solver.IntVar(0, 1, '')

# Define constraints:
# Each worker is assigned to at most 1 task
for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

# Each task is assigned to exactly one worker
for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)
    
    
# Create the objective function
objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i,j])

solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {solver.Objective().Value()}\n')
    for i in range(num_workers):
        for j in range(num_tasks):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if x[i, j].solution_value() > 0.5:
                print(f'Worker {i} assigned to task {j}.' +
                      f' Cost: {costs[i][j]}')
else:
    print('No solution found.')