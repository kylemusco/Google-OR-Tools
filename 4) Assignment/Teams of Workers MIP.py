# https://developers.google.com/optimization/assignment/assignment_teams

# Problem: 6 workers are divided into two teams and each team can perform at most two tasks

from ortools.linear_solver import pywraplp

# Rows represent how much it costs for a worker to do each task
costs = [
    [90, 76, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 105],
    [45, 110, 95, 115],
    [60, 105, 80, 75],
    [45, 65, 110, 95],
]
num_workers = len(costs)
num_tasks = len(costs[0])

team1 = [0, 2, 4]
team2 = [1, 3, 5]

# Maximum total of tasks for any team
team_max = 2

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')


# x[i, j] is an array of 0-1 variables, which will be 1
# if worker i is assigned to task j.
x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        x[worker, task] = solver.BoolVar(f'x[{worker},{task}]')
        

# Define constraints
# Each worker is assigned at most 1 task.
for worker in range(num_workers):
    solver.Add(
        solver.Sum([x[worker, task] for task in range(num_tasks)]) <= 1)

# Each task is assigned to exactly one worker.
for task in range(num_tasks):
    solver.Add(
        solver.Sum([x[worker, task] for worker in range(num_workers)]) == 1)

# Each team takes at most two tasks.
team1_tasks = []
for worker in team1:
    for task in range(num_tasks):
        team1_tasks.append(x[worker, task])
solver.Add(solver.Sum(team1_tasks) <= team_max)

team2_tasks = []
for worker in team2:
    for task in range(num_tasks):
        team2_tasks.append(x[worker, task])
solver.Add(solver.Sum(team2_tasks) <= team_max)

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
                      f' Cost = {costs[worker][task]}')
else:
    print('No solution found.')
    
print(f'Time = {solver.WallTime()} ms')