# ISyE 6644 Mini-Project 2: Pandemic Flu Spread

Robert King, Joseph Richardson, Daniel Rodgers
July 22, 2021

## Prerequesites

Requires Python ">=3.7.1,<3.10"

Execution requires the following Python packages be installed:

* argparse
* ctypes
* math
* matplotlib
* multiprocessing
* pandas
* pathlib
* Patient
* numpy
* scipy
* statistics
* sys

Optionally, you may use the included Poetry Environment Files to create the necessary virtual environment via `poetry install`:

* poetry.lock
* pyproject.toml

## Contents

* README.MD - This file.
* mp2.py - Simulation script written in Python

    ```Python
  usage: mp2.py [-h] [-ns N_STUDENTS] [-w--weekend_check WEEKEND_CHECK] [-eps EPISODES] [-nd N_DAYS] [-p P] [-sdpf SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS [SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS ...]] [-incp INCUBATION_PERIOD_GENERATORS [INCUBATION_PERIOD_GENERATORS ...]] [-infp INFECTIOUS_PERIOD_GENERATORS [INFECTIOUS_PERIOD_GENERATORS ...]]
                [-vpf VACCINATION_PROTECTION_FACTOR_GENERATORS [VACCINATION_PROTECTION_FACTOR_GENERATORS ...]]

  ISYE 6644 MiniProject2 - Flu.

  optional arguments:
    -h, --help            show this help message and exit
    -ns N_STUDENTS, --n_students N_STUDENTS
                          Number of Students
    -w--weekend_check WEEKEND_CHECK
                          Account for no school on Weekends
    -eps EPISODES, --episodes EPISODES
                          Number of episodes to simulate
    -nd N_DAYS, --n_days N_DAYS
                          Number of days to simulate
    -p P, --probability_infect P
                          Probability of Infection
    -sdpf SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS [SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS ...], --soc_dist_pro_factor SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS [SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS ...]
                          Two values between 0..1
    -incp INCUBATION_PERIOD_GENERATORS [INCUBATION_PERIOD_GENERATORS ...], --incubation_period INCUBATION_PERIOD_GENERATORS [INCUBATION_PERIOD_GENERATORS ...]
                          Two integers
    -infp INFECTIOUS_PERIOD_GENERATORS [INFECTIOUS_PERIOD_GENERATORS ...], --infection_period INFECTIOUS_PERIOD_GENERATORS [INFECTIOUS_PERIOD_GENERATORS ...]
                          Two integers
    -vpf VACCINATION_PROTECTION_FACTOR_GENERATORS [VACCINATION_PROTECTION_FACTOR_GENERATORS ...], --vax_pro_factor VACCINATION_PROTECTION_FACTOR_GENERATORS [VACCINATION_PROTECTION_FACTOR_GENERATORS ...]
                          Two values between 0..1
    ```

    Example with default parameters:

    **CAUTION: running with default parameters has required ~20 hours of processing time on an I7 3700X 8-core system**

    ```Python
    python mp2.py
    ```

    Example with modified parameters:

    ```Python
    python mp2.py -ns 1500 -w True -eps 25
    ```

* Figures Directory - Contains all figures for the default simulation parameters, with runs that do/do not have a weekend break, for 10^3..10^4 episodes.
  * Flu_Pandemic_Fig_1 - Histogram of Pandemic Length (Simulated)
  * Flu_Pandemic_means - Line Chart of Cumulative number of Mean Infections

* Data Directory - csv files generated from the Python script that were used to create Table 1 and Table 2 in the report.
  * Flu_Pandemic - CSV file of the mean infections by day for 10^3..10^4 episodes.
