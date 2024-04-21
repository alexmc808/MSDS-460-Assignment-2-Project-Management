# This Python script implements a critical path analysis modeled as a linear programming problem for a software development project 
# plan aimed at creating a restaurant recommender system. The PuLP library is used to model and solve the linear programming problem, 
# which aims to minimize the total project time considering best-case, expected, and worst-case estimates for task durations. Although 
# another objective in reality is to minimize the total cost of the project, we simplify the problem by assuming that all contributors 
# charge the same hourly rate. This simplification allows us to focus on a single objective: minimizing time. While hourly rate 
# information is included in the data, it is not utilized in the linear programming problem formulation. Therefore, the problem can be 
# attempted without assuming that all contributors charge the same hourly rate.

# Imports
from pulp import *

# Task information
tasks = {
    'A': 'Describe product',
    'B': 'Develop marketing strategy',
    'C': 'Design brochure',
    'D1': 'Requirements analysis',
    'D2': 'Software design',
    'D3': 'System design',
    'D4': 'Coding',
    'D5': 'Write documentation',
    'D6': 'Unit testing',
    'D7': 'System testing',
    'D8': 'Package deliverables',
    'E': 'Survey potential market',
    'F': 'Develop pricing plan',
    'G': 'Develop implementation plan',
    'H': 'Write client proposal'
}

predecessors = {
    'A': [],
    'B': [],
    'C': ['A'],
    'D1': ['A'],
    'D2': ['D1'],
    'D3': ['D1'],
    'D4': ['D2', 'D3'],
    'D5': ['D4'],
    'D6': ['D4'],
    'D7': ['D6'],
    'D8': ['D5', 'D7'],
    'E': ['B', 'C'],
    'F': ['D8', 'E'],
    'G': ['A', 'D8'],
    'H': ['F', 'G']
}

hourly_rates = {
    'projectManager': 46.22,
    'frontendDeveloper': 52.35,
    'backendDeveloper': 74.03,
    'dataScientist': 60.40,
    'dataEngineer': 60.12,
    'databaseAdministrator': 63.16
}

best_case_hours = {
    'A': 16,
    'B': 20,
    'C': 10,
    'D1': 10,
    'D2': 20,
    'D3': 15,
    'D4': 40,
    'D5': 20,
    'D6': 15,
    'D7': 20,
    'D8': 5,
    'E': 20,
    'F': 10,
    'G': 15,
    'H': 10
}

expected_hours = {
    'A': 40,
    'B': 50,
    'C': 20,
    'D1': 20,
    'D2': 40,
    'D3': 30,
    'D4': 120,
    'D5': 40,
    'D6': 30,
    'D7': 40,
    'D8': 10,
    'E': 40,
    'F': 20,
    'G': 30,
    'H': 20
}

worst_case_hours = {
    'A': 80,
    'B': 100,
    'C': 40,
    'D1': 40,
    'D2': 80,
    'D3': 60,
    'D4': 240,
    'D5': 80,
    'D6': 60,
    'D7': 80,
    'D8': 20,
    'E': 80,
    'F': 40,
    'G': 60,
    'H': 40
}

# Create a list of tasks
tasks_list = list(tasks.keys())

#########################

# Create the LP problem for best case scenario
prob_b = LpProblem("Critical Path Best Case", LpMinimize)

# Create the LP variables
start_times_b = {task: LpVariable(f"start_{task}_b", 0, None) for task in tasks_list}
end_times_b = {task: LpVariable(f"end_{task}_b", 0, None) for task in tasks_list}

# Add the constraints
for task in tasks_list:
    prob_b += end_times_b[task] == start_times_b[task] + best_case_hours[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_b += start_times_b[task] >= end_times_b[predecessor], f"{task}_predecessor_{predecessor}"

# Set the objective function
prob_b += lpSum([end_times_b[task] for task in tasks_list]), "minimize_end_times"

# Solve the LP problem
status = prob_b.solve()

# Print the results
print("Critical Path time:")
for task in tasks_list:
    if value(start_times_b[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_b[task]) == max([value(end_times_b[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_b[task])} hours in duration")

# Print solution
print("\nSolution variable values (Best Case):")
for var in prob_b.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

#########################

# Create the LP problem for expected case scenario
prob_e = LpProblem("Critical Path Expected Case", LpMinimize)

# Create the LP variables
start_times_e = {task: LpVariable(f"start_{task}_e", 0, None) for task in tasks_list}
end_times_e = {task: LpVariable(f"end_{task}_e", 0, None) for task in tasks_list}

# Add the constraints
for task in tasks_list:
    prob_e += end_times_e[task] == start_times_e[task] + expected_hours[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_e += start_times_e[task] >= end_times_e[predecessor], f"{task}_predecessor_{predecessor}"

# Set the objective function
prob_e += lpSum([end_times_e[task] for task in tasks_list]), "minimize_end_times"

# Solve the LP problem
status = prob_e.solve()

# Print the results
print("Critical Path time:")
for task in tasks_list:
    if value(start_times_e[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_e[task]) == max([value(end_times_e[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_e[task])} hours in duration")

# Print solution
print("\nSolution variable values (Expected Case):")
for var in prob_e.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

#########################