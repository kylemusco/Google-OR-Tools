# https://developers.google.com/optimization/assignment/assignment_example

# Problem: Assign works at most one task, with no two workers performing the same task,
# while minimizing the total cost using the CP-SAT solver

from ortools.sat.python import cp_model

model = cp_model.CpModel()

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

# Define the variables
x = []
for i in range(num_workers):
    t = []
    for j in range(num_tasks):
        t.append(model.NewBoolVar(f'x[{i},{j}]'))
    x.append(t)
   
# Define the constraints 
# Each worker is assigned to at most one task.
for i in range(num_workers):
    model.AddAtMostOne(x[i][j] for j in range(num_tasks))

# Each task is assigned to exactly one worker.
for j in range(num_tasks):
    model.AddExactlyOne(x[i][j] for i in range(num_workers))
    
# Define objective function
objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i][j])

model.Minimize(sum(objective_terms))

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Total cost = {solver.ObjectiveValue()}')
    print()
    for i in range(num_workers):
        for j in range(num_tasks):
            if solver.BooleanValue(x[i][j]):
                print(
                    f'Worker {i} assigned to task {j} Cost = {costs[i][j]}')
else:
    print('No solution found.')