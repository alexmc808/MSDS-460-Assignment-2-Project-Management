# MSDS 460 Assignment 2: Network Models - Project Management

This repository contains files associated with the project management assignment for MSDS 460, which focuses on applying linear programming techniques to a network model for critical path analysis in project management.

## Problem Setup

The initial step in this assignment was completing an Excel spreadsheet detailing the best-case, expected, and worst-case completion times for fifteen tasks necessary for developing a restaurant recommender system. The spreadsheet also includes information about required roles and their hourly costs. Roles include project manager, frontend developer, backend developer, data scientist, data engineer, and database administrator. Access to the completed spreadsheet is available under "Complete_Project_Plan.xlsx".

## Model Specification

The following setup is the standard form of the linear programming (LP) problem:

- Decision Variables:
  - Si = start time for task i 
  - Ei = end time for task i
- Objective Function:
  - Minimize
    - T = Σ Ei
    - T = Σ Hi × Rj (where Rj represents the hourly rate for role j)
- Subject to:
  - Ei = Si + Hi for all tasks i (where Hi represents the best-case, expected, or worst-case time estimate for task i)
  - Si > Ej for all tasks i, j where i is a successor of j
  - Si, Ei > 0 for all tasks i (non-negativity constraints)

## Programming

To implement the LP problem, Python and Python's PuLP package is utilized. The program code and output can be found under “Critical_Path_Analysis_Code.py” and “Critical_Path_Analysis_Solution.txt". There are three different LP problems and solutions to represent the three different task completion scenarios of best-case, expected, and worst-case. 

## Solution

With a minimum-time objective, the best-case scenario minimum total project time is 151 hours. The expected minimum total project time is 350 hours. Finally, the worst-case scenario minimum total project time is 700 hours. Regardless of the scenario, the critical path remains the same, consisting of tasks A → D1 → D2 → D4 → D6 → D7 → D8 → G → H. This is the critical path because it reflects the longest sequence of dependent tasks that must be completed to execute a project. To help visualize the solutions, Gantt charts, found under "Gantt_Charts.xlsx" can be referenced. 

## Overview (Mock Discussion with Prospective Client)
A mock discussion with a prospective client is included to detail the project's objectives, technology stack, estimated completion times, and associated costs for the various scenarios. 
