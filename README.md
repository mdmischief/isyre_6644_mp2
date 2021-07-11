# ISyE 6644 Mini-Project 1: Pandemic Flu Spread

Robert King, Joseph Richardson, Daniel Rodgers
June 24, 2021

## Prerequesites

Requires Python ">=3.7.1,<3.10"

Execution requires the following PYthon packages be installed:

* numpy
* matplotlib
* pandas
* scipy
* statistics
* argparse
* pathlib

Optionally, you may use the included Poetry Environment Files:

* poetry.lock
* pyproject.toml

## Contents

* README.MD - This file.
* mp1.py - Simulation script written in Python

    ```Python
    usage: mp1.py [-h] [-ns N_STUDENTS] [-w WEEKEND_CHECK] [-eps EPISODES] [-nd N_DAYS] [-p P] [-ndi N_DAYS_INFECTIOUS]

    ISYE 6644 MiniProject - Flu.

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
                              Probabilty of Infection
        -mpf MASK_PROTECTION_FACTOR_GENERATORS [MASK_PROTECTION_FACTOR_GENERATORS ...], --mask_pro_factor MASK_PROTECTION_FACTOR_GENERATORS [MASK_PROTECTION_FACTOR_GENERATORS ...]
                              Two values between 0..1
        -sdpf SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS [SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS ...], --soc_dist_pro_factor SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS [SOCIAL_DISTANCE_PROTECTION_FACTOR_GENERATORS ...]
                              Two values between 0..1
        -hdpf HANDWASH_DISTANCE_PROTECTION_FACTOR_GENERATORS [HANDWASH_DISTANCE_PROTECTION_FACTOR_GENERATORS ...], --hand_wash_pro_factor HANDWASH_DISTANCE_PROTECTION_FACTOR_GENERATORS [HANDWASH_DISTANCE_PROTECTION_FACTOR_GENERATORS ...]
                              Two values between 0..1
        -incp INCUBATION_PERIOD_GENERATORS [INCUBATION_PERIOD_GENERATORS ...], --incubation_period INCUBATION_PERIOD_GENERATORS [INCUBATION_PERIOD_GENERATORS ...]
                              Two values between 0..1 and an int
        -infp INFECTIOUS_PERIOD_GENERATORS [INFECTIOUS_PERIOD_GENERATORS ...], --infection_period INFECTIOUS_PERIOD_GENERATORS [INFECTIOUS_PERIOD_GENERATORS ...]
                              Two values between 0..1 and an int
        -vpf VACCINATION_PROTECTION_FACTOR_GENERATORS [VACCINATION_PROTECTION_FACTOR_GENERATORS ...], --vax_pro_factor VACCINATION_PROTECTION_FACTOR_GENERATORS [VACCINATION_PROTECTION_FACTOR_GENERATORS ...]
                              Two values between 0..1
    ```

    Example with default parameters:

    ```Python
    python mp1.py
    ```

    Example with modified parameters:

    ```Python
    python mp1.py -ns 30 -p 0.10 -w False -ndi 5 -eps 100000
    ```

* Figures Directory - Contains all figures for the default simulation parameters, with runs that do/do not have a weekend break, for 10^3..10^6 runs.
  * Flu_Pandemic_Fig_1 - Histogram of Pandemic Length (Simulated)
  * Flu_Pandemic_Fig_1_smallbins - Histogram of Pandemic Length with increased number of bins (Simulated)
  * Flu_Pandemic_Fig_2 - Histogram of First Two Days of Pandemic (Theorectical)
  * Flu_Pandemic_Fig_2 - Histogram of First Two Days of Pandemic (Empirical)
  * Flu_Pandemic_means - Line Chart of Cumulative number of Mean Infections

* Tables Directory - csv files generated from the Python script that were used to create Table 1 and Table 2 in the report.
  * day2_dist.csv - The theoretical distribution of kids infected by day 2 (Table 1)
  * p_range.csv - Percent of episodes that ended in all kids infected for simulations at different infection rates, p. Based on Monte Carlo simulations of 1000 episodes each. (Table 2)
