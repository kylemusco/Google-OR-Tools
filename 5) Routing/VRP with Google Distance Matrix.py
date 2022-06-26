# https://developers.google.com/optimization/routing/vrp#distance_matrix_api

# Problem: Use the Google Distance Matrix API to generate distance matrix from addresses for VRP

from __future__ import division
from __future__ import print_function
import requests
import json
import urllib

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data():
  data = {}
  data['API_key'] = 'YOUR API KEY' # Get API key here: https://developers.google.com/maps/documentation/distance-matrix/start#get-a-key
  data['addresses'] = ['3610+Hacks+Cross+Rd+Memphis+TN',  # depot
                       '1921+Elvis+Presley+Blvd+Memphis+TN',
                       '149+Union+Avenue+Memphis+TN',
                       '1034+Audubon+Drive+Memphis+TN',
                       '1532+Madison+Ave+Memphis+TN',
                       '706+Union+Ave+Memphis+TN',
                       '3641+Central+Ave+Memphis+TN',
                       '926+E+McLemore+Ave+Memphis+TN',
                       '4339+Park+Ave+Memphis+TN',
                       '600+Goodwyn+St+Memphis+TN',
                       '2000+North+Pkwy+Memphis+TN',
                       '262+Danny+Thomas+Pl+Memphis+TN',
                       '125+N+Front+St+Memphis+TN',
                       '5959+Park+Ave+Memphis+TN',
                       '814+Scott+St+Memphis+TN',
                       '1005+Tillman+St+Memphis+TN'
                      ]
  data['num_vehicles'] = 4
  data['depot'] = 0
  
  return data


def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)  # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix



def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
        address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
                       
    with urllib.request.urlopen(request) as url:
        jsonResult = url.read()
        response = json.loads(jsonResult)
        return response

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def print_solution(data, manager, routing, solution):
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    total_distance_traveled = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance_traveled += route_distance
        max_route_distance = max(route_distance, max_route_distance)
        
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    print('Total distance traveled: {}m'.format(total_distance_traveled))

# Define data model
data = create_data()

# Populate distance matrix from Google's Distance Matrix API
# data['distance_matrix'] = create_distance_matrix(data)
data['distance_matrix'] =  [
    [0, 24127, 33358, 14942, 31967, 32005, 19117, 28405, 15322, 21145, 28891, 34750, 35275, 10539, 26713, 27274], 
    [25143, 0, 8310, 10784, 6920, 6957, 10701, 3271, 10762, 7929, 11795, 9703, 10228, 19021, 11390, 13658], 
    [34053, 8483, 0, 14083, 4083, 1353, 11028, 4235, 13853, 9680, 8131, 1809, 1076, 27931, 9697, 10046], 
    [15492, 11581, 13936, 0, 11066, 12583, 4144, 10972, 636, 5283, 10935, 15657, 16181, 6013, 9150, 9523], 
    [33339, 5882, 4084, 11348, 0, 2731, 7388, 4364, 11118, 6193, 4574, 5082, 5606, 20764, 6140, 7127], 
    [32700, 7130, 1353, 12730, 2730, 0, 9675, 3676, 12500, 8327, 7717, 2423, 2288, 26578, 8883, 9580], 
    [19455, 10707, 11038, 4135, 7421, 9685, 0, 9189, 3905, 2777, 7339, 10986, 11463, 8764, 5555, 5850], 
    [29097, 3271, 4253, 11459, 4364, 3930, 9183, 0, 11229, 6411, 9752, 5328, 5193, 22975, 10376, 11614], 
    [15872, 11351, 13706, 636, 10836, 12353, 3914, 10742, 0, 5053, 10705, 15427, 15951, 5496, 8920, 9293], 
    [21886, 7929, 9458, 5283, 6226, 8105, 2777, 6411, 5053, 0, 7057, 11179, 11704, 10430, 5033, 6378], 
    [28955, 12653, 7660, 10807, 4137, 6889, 7315, 8255, 10577, 6697, 0, 6473, 7288, 18418, 3363, 3406], 
    [35603, 10033, 1856, 15695, 5135, 2421, 11235, 5292, 15465, 11292, 6975, 0, 1540, 29525, 8542, 8890]
]

# Define routing index manager
manager = pywrapcp.RoutingIndexManager(
    len(data['distance_matrix']), data['num_vehicles'], data['depot'])

# Define routing model
routing = pywrapcp.RoutingModel(manager)

# Create and register a transit callback
def distance_callback(from_index, to_index):
    # Returns the distance between the two nodes
    # Convert from routing variable Index to distance matrix NodeIndex
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

# Define cost of each arc
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Add Distance constraint
dimension_name = 'Distance'
routing.AddDimension(
    transit_callback_index,
    0,       # no slack
    70000,   # vehicle maximum travel distance
    True,    # start cumul to zero
    dimension_name)
distance_dimension = routing.GetDimensionOrDie(dimension_name)
distance_dimension.SetGlobalSpanCostCoefficient(100)

# Setting first solution heuristic.
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

solution = routing.SolveWithParameters(search_parameters)

if solution:
    print_solution(data, manager, routing, solution)
else:
    print('No solution found')