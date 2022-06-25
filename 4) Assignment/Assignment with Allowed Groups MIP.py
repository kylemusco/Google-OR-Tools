# https://developers.google.com/optimization/assignment/assignment_groups

# Problem: Find the minimum cost to assign workers to tasks where all workers have to belong to one of 3 assignment groups

from ortools.linear_solver import pywraplp

# Define data
costs = [
    [90, 76, 75, 70, 50, 74],
    [35, 85, 55, 65, 48, 101],
    [125, 95, 90, 105, 59, 120],
    [45, 110, 95, 115, 104, 83],
    [60, 105, 80, 75, 59, 62],
    [45, 65, 110, 95, 47, 31],
    [38, 51, 107, 41, 69, 99],
    [47, 85, 57, 71, 92, 77],
    [39, 63, 97, 49, 118, 56],
    [47, 101, 71, 60, 88, 109],
    [17, 39, 103, 64, 61, 92],
    [101, 45, 83, 59, 92, 27],
]
num_workers = len(costs)
num_tasks = len(costs[0])

# Define groups
group1 = [  # Subgroups of workers 0 - 3
    [2, 3],
    [1, 3],
    [1, 2],
    [0, 1],
    [0, 2],
]

group2 = [  # Subgroups of workers 4 - 7
    [6, 7],
    [5, 7],
    [5, 6],
    [4, 5],
    [4, 7],
]

group3 = [  # Subgroups of workers 8 - 11
    [10, 11],
    [9, 11],
    [9, 10],
    [8, 10],
    [8, 11],
]

# Create the mip solver with the SCIP backend
solver = pywraplp.Solver.CreateSolver('SCIP')

# x[worker, task] is an array of 0-1 variables, which will be 1
# if the worker is assigned to the task
x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        x[worker, task] = solver.BoolVar(f'x[{worker},{task}]')
        
# Define constraints
# The total size of the tasks each worker takes on is at most total_size_max
for worker in range(num_workers):
    solver.Add(
        solver.Sum([x[worker, task] for task in range(num_tasks)]) <= 1)

# Each task is assigned to exactly one worker
for task in range(num_tasks):
    solver.Add(
        solver.Sum([x[worker, task] for worker in range(num_workers)]) == 1)
    
# Define objective
objective_terms = []
for worker in range(num_workers):
    for task in range(num_tasks):
        objective_terms.append(costs[worker][task] * x[worker, task])
solver.Minimize(solver.Sum(objective_terms))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f'Total cost = {solver.Objective().Value()}\n')
    for worker in range(num_workers):
        for task in range(num_tasks):
            if x[worker, task].solution_value() > 0.5:
                print(f'Worker {worker} assigned to task {task}.' +
                      f' Cost: {costs[worker][task]}')
else:
    print('No solution found.')
    
print(f'Time = {solver.WallTime()} ms')