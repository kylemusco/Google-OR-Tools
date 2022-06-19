# A linear optimization problem is one in which the objective function and the constraints are linear expressions in the variables.
# aka Figuring out the best solution to a problem modeled as a set of linear relationships
# Problem:
# Maximize 3x + y subject to the following constraints:
# 0	≤ x	≤ 1
# 0	≤ y	≤ 2
# x + y	≤ 2

from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit

# Create the linear solver with the GLOP backend.
solver = pywraplp.Solver.CreateSolver('GLOP')

# Create the variables x and y.
x = solver.NumVar(0, 1, 'x')
y = solver.NumVar(0, 2, 'y')

print('Number of variables =', solver.NumVariables())

# Create a linear constraint, 0 <= x + y <= 2.
ct = solver.Constraint(0, 2, 'ct')
ct.SetCoefficient(x, 1)
ct.SetCoefficient(y, 1)

print('Number of constraints =', solver.NumConstraints())

# Create the objective function, 3 * x + y.
objective = solver.Objective()
objective.SetCoefficient(x, 3)
objective.SetCoefficient(y, 1)
objective.SetMaximization()

solver.Solve()
print('Solution:')
print('Objective value =', objective.Value())
print('x =', x.solution_value())
print('y =', y.solution_value())