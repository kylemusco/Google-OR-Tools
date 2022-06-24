# https://developers.google.com/optimization/mip/mip_example

# Solves the same problem as the previous file but without the integer constraint

from ortools.linear_solver import pywraplp

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create the linear solver with the GLOP backend.
solver = pywraplp.Solver.CreateSolver('GLOP')

infinity = solver.infinity()
# x and y are integer non-negative variables.
x = solver.IntVar(0.0, infinity, 'x')
y = solver.IntVar(0.0, infinity, 'y')

print('Number of variables =', solver.NumVariables())

infinity = solver.infinity()
# Create the variables x and y.
x = solver.NumVar(0.0, infinity, 'x')
y = solver.NumVar(0.0, infinity, 'y')

print('Number of variables =', solver.NumVariables())