# https://developers.google.com/optimization/lp/lp_example

# Maximize 3x+4y subject to the following constraints:
# x+2y ≤ 14
# 3x–y ≥ 0
# x–y ≤ 2

from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

# Create the linear solver with the GLOP backend.
solver = pywraplp.Solver.CreateSolver('GLOP')

# Create the variables x and y.
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

print('Number of variables =', solver.NumVariables())

# Define constraints
# x+2y <= 14
solver.Add(x + 2 * y <= 14.0)

# 3x-y >= 0
solver.Add(3 * x - y >= 0.0)

# x-y <= 2.
solver.Add(x - y <= 2.0)

print('Number of constraints =', solver.NumConstraints())

# Create the objective function, 3x+4y
objective = solver.Objective()
objective.SetCoefficient(x, 3)
objective.SetCoefficient(y, 4)
objective.SetMaximization()

solver.Solve()
print('Solution:')
print('Objective value =', objective.Value())
print('x =', x.solution_value())
print('y =', y.solution_value())