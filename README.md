
## Bank Simulation Project

This repository contains the Python code for a simulation of banking operations. The simulation models the interactions between customers and bank employees to optimize service delivery and customer satisfaction.
**Project Description:**
- **Purpose:** Simulate the operation of a bank branch to improve the allocation of employees and customer satisfaction. This involves simulating various banking processes such as deposits and withdrawals.
- **Details:** Employees are assigned to different processes, each having varying levels of expertise. The system analyzes the time each employee spends on each process and the intervals between customer arrivals.
- **Objective:** Determine the best strategy for assigning employees to customers.
- **Requirements:** Implement classes for "Employee", "Customer", and "System" with specified methods and attributes.
### Components

- `bank.py`: Main program file containing the logic for bank operations and process simulations.
- `plot.py`: Utility script for generating charts that visualize the outcomes of different simulation strategies.

### Classes

- **ParameterLoader**: Loads system parameters from text files and initializes system settings.
- **RandomGenerator**: Generates random numbers for simulating various aspects of the bank operations, such as service times and customer arrival intervals.
- **Queue**: Manages the queue of customers within the bank, handling operations like adding or removing customers from the queue.
- **Decide**: Implements different strategies for assigning employees to customers, optimizing based on criteria like wait time or service speed.

### Running the Simulation

1. Ensure Python 3.x is installed.
2. Install required libraries if necessary.
3. Run `bank.py` to start the simulation.
4. To view charts let `plot.py` to run fully.
5. Use `wait()` for mean eaiting time chart, `free()` for mean free time of tellers, `money()` for the probability of depositing money and `queue()` for probability of entering the queue.
   
### Contribution

This project is part of an academic assignment. Contributions and suggestions are welcome to improve the simulation and its outcomes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
