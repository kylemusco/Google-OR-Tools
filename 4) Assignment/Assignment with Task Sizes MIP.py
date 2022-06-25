# https://developers.google.com/optimization/assignment/assignment_cp

# Problem: Assign tasks to workers such that the overall cost is minimized. In this example, tasks have a "size" value associated with them
# "Size" can represent any secondary constraint (Such as time, weight, volume, etc). The max task "size" a worker can be assigned is 15

from ortools.linear_solver import pywraplp

# Define data
costs = [
    [90, 76, 75, 70, 50, 74, 12, 68],
    [35, 85, 55, 65, 48, 101, 70, 83],
    [125, 95, 90, 105, 59, 120, 36, 73],
    [45, 110, 95, 115, 104, 83, 37, 71],
    [60, 105, 80, 75, 59, 62, 93, 88],
    [45, 65, 110, 95, 47, 31, 81, 34],
    [38, 51, 107, 41, 69, 99, 115, 48],
    [47, 85, 57, 71, 92, 77, 109, 36],
    [39, 63, 97, 49, 118, 56, 92, 61],
    [47, 101, 71, 60, 88, 109, 52, 90],
]
num_workers = len(costs)
num_tasks = len(costs[0])

task_sizes = [10, 7, 3, 12, 15, 4, 11, 5]
# Maximum total of task sizes for any worker
total_size_max = 15

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define variables
# x[i, j] is an array of 0-1 variables, which will be 1
# if worker i is assigned to task j.
x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        x[worker, task] = solver.BoolVar(f'x[{worker},{task}]')
        
# The total size of the tasks each worker takes on is at most total_size_max.
for worker in range(num_workers):
    solver.Add(
        solver.Sum([
            task_sizes[task] * x[worker, task] for task in range(num_tasks)
        ]) <= total_size_max)

# Each task is assigned to exactly one worker.
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