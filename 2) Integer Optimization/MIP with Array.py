# https://developers.google.com/optimization/mip/mip_var_array

# Problem: Maximize 7x(1) + 8x(2) + 2x(3) + 9x(4) + 6x(5) subject to the following constraints:
# 5x(1) + 7x(2) + 9x(3) + 2x(4) + 1x(5) ≤ 250
# 18x(1) + 4x(2) - 9x(3) + 10x(4) + 12x(5) ≤ 285
# 4x(1) + 7x(2) + 3x(3) + 8x(4) + 5x(5) ≤ 211
# 5x(1) + 13x(2) + 16x(3) + 3x(4) - 7x(5) ≤ 315
# where x1, x2, ..., x5 are non-negative integers.

from ortools.linear_solver import pywraplp

def create_data_model():
    # Stores the data for the problem
    data = {}
    data['constraint_coeffs'] = [
        [5, 7, 9, 2, 1],
        [18, 4, -9, 10, 12],
        [4, 7, 3, 8, 5],
        [5, 13, 16, 3, -7]
    ]
    data['bounds'] = [250, 285, 211, 315]
    data['obj_coeffs'] = [7, 8, 2, 9, 6]
    data['num_vars'] = 5
    data['num_constraints'] = 4
    return data

data = create_data_model()

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define the variables
infinity = solver.infinity()
x = {}
for j in range(data['num_vars']):
    x[j] = solver.IntVar(0, infinity, 'x[%i]' % j)
print('Number of variables =', solver.NumVariables())

# Define the constraints
for i in range(data['num_constraints']):
    constraint = solver.RowConstraint(0, data['bounds'][i], '')
    for j in range(data['num_vars']):
        constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
print('Number of constraints =', solver.NumConstraints())

# Define the objective
objective = solver.Objective()
for j in range(data['num_vars']):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j])
objective.SetMaximization()

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Objective value =', solver.Objective().Value())
    for j in range(data['num_vars']):
        print(x[j].name(), ' = ', x[j].solution_value())
    print()
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
else:
    print('The problem does not have an optimal solution.')