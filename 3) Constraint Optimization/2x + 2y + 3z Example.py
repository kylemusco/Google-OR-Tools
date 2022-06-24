# https://developers.google.com/optimization/cp/cp_example

# Problem: Maximize 2x + 2y + 3z subject to the following constraints:
# x + 7⁄2 y + 3⁄2 z	≤ 50
# 3x - 5y + 7z ≤ 45
# 5x + 2y - 6z ≤ 37
# x, y, z ≥ 0
# x, y, z are integers

from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Create the variables
var_upper_bound = max(50, 45, 37)
x = model.NewIntVar(0, var_upper_bound, 'x')
y = model.NewIntVar(0, var_upper_bound, 'y')
z = model.NewIntVar(0, var_upper_bound, 'z')

# Define the constraints
model.Add(2 * x + 7 * y + 3 * z <= 50)
model.Add(3 * x - 5 * y + 7 * z <= 45)
model.Add(5 * x + 2 * y - 6 * z <= 37)

# Define the objective function
model.Maximize(2 * x + 2 * y + 3 * z)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
    print(f'x = {solver.Value(x)}')
    print(f'y = {solver.Value(y)}')
    print(f'z = {solver.Value(z)}')
else:
    print('No solution found.')
    
# Statistics
print('\nStatistics')
print(f'  status: {solver.StatusName(status)}')
print(f'  conflicts: {solver.NumConflicts()}')
print(f'  branches: {solver.NumBranches()}')
print(f'  wall time: {solver.WallTime()} s')