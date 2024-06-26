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

# Create the LP problem for worst case scenario
prob_w = LpProblem("Critical Path Worst Case", LpMinimize)

# Create the LP variables
start_times_w = {task: LpVariable(f"start_{task}_w", 0, None) for task in tasks_list}
end_times_w = {task: LpVariable(f"end_{task}_w", 0, None) for task in tasks_list}

# Add the constraints
for task in tasks_list:
    prob_w += end_times_w[task] == start_times_w[task] + worst_case_hours[task], f"{task}_duration"
    for predecessor in predecessors[task]:
        prob_w += start_times_w[task] >= end_times_w[predecessor], f"{task}_predecessor_{predecessor}"

# Set the objective function
prob_w += lpSum([end_times_w[task] for task in tasks_list]), "minimize_end_times"

# Solve the LP problem
status = prob_w.solve()

# Print the results
print("Critical Path time:")
for task in tasks_list:
    if value(start_times_w[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times_w[task]) == max([value(end_times_w[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times_w[task])} hours in duration")

# Print solution
print("\nSolution variable values (Expected Case):")
for var in prob_w.variables():
    if var.name != "_dummy":
        print(var.name, "=", var.varValue)

#########################

# Open a file to write the solution output for the three problems
with open('Critical_Path_Analysis_Solution.txt', 'w') as file:
    for prob, case in zip([prob_b, prob_e, prob_w], ["Best Case", "Expected Case", "Worst Case"]):
        file.write(f"Problem: {case} Scenario\n")
        file.write(f"Status = {LpStatus[prob.status]}\n")
        file.write("Start and end times for each task (hours):\n")
        for task in tasks_list:
            if prob == prob_b:
                start_time = value(start_times_b[task])
                end_time = value(end_times_b[task])
            elif prob == prob_e:
                start_time = value(start_times_e[task])
                end_time = value(end_times_e[task])
            elif prob == prob_w:
                start_time = value(start_times_w[task])
                end_time = value(end_times_w[task])
            file.write(f"{task} ({tasks[task]}):\n    Start = {start_time}\n    End = {end_time}\n")
        file.write(f"Minimum total project time = {end_time} hours\n")
        file.write("\n")
#########################

# Cost estimates
# Using the hourly_rates defined above, calculate an estimated cost to charge a prospective client for each of the three scenarios.

# Provide information on how many of each role works on each task
roles_included = {
    'A': {'projectManager': 1},
    'B': {'projectManager': 1},
    'C': {'frontendDeveloper': 1},
    'D1': {'projectManager': 1, 'dataScientist': 1, 'dataEngineer': 1},
    'D2': {'projectManager': 1, 'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1, 'dataEngineer': 1, 'databaseAdministrator': 1},
    'D3': {'projectManager': 1, 'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataEngineer': 1, 'databaseAdministrator': 1},
    'D4': {'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1, 'dataEngineer': 1},
    'D5': {'projectManager': 1, 'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1, 'dataEngineer': 1},
    'D6': {'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1, 'dataEngineer': 1},
    'D7': {'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1},
    'D8': {'projectManager': 1},
    'E': {'projectManager': 1},
    'F': {'projectManager': 1, 'databaseAdministrator': 1},
    'G': {'projectManager': 1, 'frontendDeveloper': 1, 'backendDeveloper': 1, 'dataScientist': 1, 'dataEngineer': 1},
    'H': {'projectManager': 1}
}

# Calculate the total cost for the project (best-case)
total_cost_best = round(sum(best_case_hours[task] * sum(hourly_rates[role] for role in roles_included[task]) for task in best_case_hours.keys()), 2)

# Calculate the total cost for the project (expected)
total_cost_expected = round(sum(expected_hours[task] * sum(hourly_rates[role] for role in roles_included[task]) for task in expected_hours.keys()), 2)

# Calculate the total cost for the project (worst-case)
total_cost_worst = round(sum(worst_case_hours[task] * sum(hourly_rates[role] for role in roles_included[task]) for task in worst_case_hours.keys()), 2)

# Open a file to write the total cost estimate for the three scenarios
with open("Total_Cost_Summary.txt", "w") as file:
    file.write("Total Cost Summary:\n")
    file.write(f"Best-Case Scenario: ${total_cost_best}\n")
    file.write(f"Expected Scenario: ${total_cost_expected}\n")
    file.write(f"Worst-Case Scenario: ${total_cost_worst}\n")