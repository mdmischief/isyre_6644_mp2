import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import binom
from statistics import median
import argparse
import pathlib
from patient.patient import Patient

fig_dir = pathlib.Path.cwd() / 'figs'
fig_dir.mkdir(parents=True, exist_ok=True)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(
    prog='mp2.py',
    description='ISYE 6644 MiniProject2 - Flu.'
)
parser.add_argument(
    "-ns",
    "--n_students",
    required=False,
    help="Number of Students",
    type=int,
    dest='n_students',
    default=21,
)
parser.add_argument(
    "-w"
    "--weekend_check",
    required=False,
    help="Account for no school on Weekends",
    type=str2bool,
    dest='weekend_check',
    default=False
)
parser.add_argument(
    "-eps",
    "--episodes",
    required=False,
    help="Number of episodes to simulate",
    type=int,
    dest='episodes',
    default=10000
)
parser.add_argument(
    "-nd",
    "--n_days",
    required=False,
    help="Number of days to simulate",
    type=int,
    dest='n_days',
    default=63
)
parser.add_argument(
    "-p",
    "--probability_infect",
    required=False,
    help="Probabilty of Infection",
    type=float,
    dest='p',
    default=0.02
)
parser.add_argument(
    "-ndi",
    "--n_days_infectious",
    required=False,
    help="Number of days infectious",
    type=int,
    dest='n_days_infectious',
    default=3
)

args = vars(parser.parse_args())
n_students = args['n_students']
weekend_check = args['weekend_check']
eps = args['episodes']
n_days = args['n_days']
p = args['p']


# for pt in population:
#     print(repr(pt))


def sim_day(population, day=0):
    if weekend_check and day != 0 and (day+1) % 6 == 0:
        # do nothing
        # print(f'Day = {day}: 6 do nothing')
        pass
    elif weekend_check and day != 0 and (day+1) % 7 == 0:
        # do nothing
        # print(f'Day = {day}: 7 do nothing')
        pass
    else:
        # print(f'Day = {day}: do the thing')
        for pt in population:
            for peer in population:
                pt.encounter(peer=peer, simulation_timehack=day)


# def main():
population = []

for i in range(0, n_students):
    population.append(
        Patient(
            id=i,
            name=i,
            infectious_probability=.8
        )
    )

population[0].patient_zero(0)

for i in range(0, 20):
    print(f'Timehack: {i}')
    sim_day(population, i)

    for pt in population:
        print(pt)
