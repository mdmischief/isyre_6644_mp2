import numpy as np
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
from statistics import median
import argparse
import pathlib
import multiprocessing as mp
from patient.patient import Patient
import sys
import ctypes

fig_dir = pathlib.Path.cwd() / 'figs'
fig_dir.mkdir(parents=True, exist_ok=True)

data_dir = pathlib.Path.cwd() / 'data'
data_dir.mkdir(parents=True, exist_ok=True)


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
    default=1500,
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
    default=60
)
parser.add_argument(
    "-p",
    "--probability_infect",
    required=False,
    help="Probability of Infection",
    type=float,
    dest='p',
    default=0.083   # Median Value of 95% CI from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5934309/
)
parser.add_argument(
    "-sdpf",
    "--soc_dist_pro_factor",
    required=False,
    help='Two values between 0..1',
    type=float,
    nargs='+',
    dest='social_distance_protection_factor_generators',
    default=[0.0, 0.1]
)
parser.add_argument(
    "-incp",
    "--incubation_period",
    required=False,
    help='Two integers',
    type=float,
    nargs='+',
    dest='incubation_period_generators',
    default=[2, 5]
)
parser.add_argument(
    "-infp",
    "--infection_period",
    required=False,
    help='Two integers',
    type=float,
    nargs='+',
    dest='infectious_period_generators',
    default=[2, 5]
)
parser.add_argument(
    "-vpf",
    "--vax_pro_factor",
    required=False,
    help='Two values between 0..1',
    type=float,
    nargs='+',
    dest='vaccination_protection_factor_generators',
    default=[0.44, 0.48]  # https://pubmed.ncbi.nlm.nih.gov/9580647/
)


args = vars(parser.parse_args())
n_students = args['n_students']
weekend_check = args['weekend_check']
eps = args['episodes']
n_days = args['n_days']
p = args['p']
social_distance_protection_factor_generators = args['social_distance_protection_factor_generators']
incubation_period_generators = args['incubation_period_generators']
infectious_period_generators = args['infectious_period_generators']
vaccination_protection_factor_generators = args['vaccination_protection_factor_generators']


def shared_array(dtype, shape):
    """
    Form a shared memory numpy array.

    https://stackoverflow.com/q/5549190/2506522
    """

    size = sys.getsizeof(dtype())
    for dim in shape:
        size *= dim

    shared_array_base = mp.Array(ctypes.c_float, size)
    shared_array = np.ndarray(shape, dtype=dtype, buffer=shared_array_base.get_obj())
    shared_array = shared_array.reshape(*shape)
    return shared_array


day_results = None


def init(day_results_base):
    global lock
    lock = mp.Lock()
    global day_results
    day_results = np.ctypeslib.as_array(day_results_base.get_obj())
    day_results = day_results.reshape(eps, n_days)


def sim_day(population, infections, day=0):

    if weekend_check and day != 0 and (day + 1) % 6 == 0:
        # do nothing
        # print(f'Day = {day}: 6 do nothing')
        pass
    elif weekend_check and day != 0 and (day + 1) % 7 == 0:
        # do nothing
        # print(f'Day = {day}: 7 do nothing')
        pass
    else:
        # print(f'Day = {day}: do the thing')
        for pt in population:
            for peer in population:
                infections += pt.encounter(peer=peer, simulation_timehack=day)

    return infections


def episode(i, def_param=shared_array):
    population = []
    infections = np.zeros(n_days)

    for j in range(0, n_students):
        # Calculate handwashing protection factor.
        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4839906/
        # 42% of population 0-3, 58% of population 4-9
        # 0-3: OR == 0.26
        # 4-9: OR == 0.029
        handwash_protection_factor = 0

        _cat_low = ceil(np.random.uniform(0.0, .3) * 10)
        _cat_high = ceil(np.random.uniform(.4, .9) * 10)

        if np.random.uniform(0, 1) <= .42:
            handwash_protection_factor = _cat_low * 0.26
        else:
            handwash_protection_factor = 0.78 + ((_cat_high - 3) * .029)

        # Calculate mask wearing protection factor.
        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7169241/
        # 50% of population, 60-80% effectivity
        mask_protection_factor = 0
        if ceil(np.random.uniform()) >= 0.5:
            mask_protection_factor = np.random.uniform(0.6, 0.8)

        population.append(
            Patient(
                id=j,
                name=j,
                infectious_probability=p,
                mask_protection_factor=mask_protection_factor,
                social_distance_protection_factor_generators=social_distance_protection_factor_generators,
                handwash_protection_factor=handwash_protection_factor,
                incubation_period_generators=incubation_period_generators,
                infectious_period_generators=infectious_period_generators,
                vaccination_protection_factor_generators=vaccination_protection_factor_generators
            )
        )

        if j != 0 and np.random.uniform(0, 1) <= .68:
            population[j].vaccinate(j)

            if np.random.uniform() >= 0.50:
                population[j].vaccinate(j)

    population[0].patient_zero(0)

    for simulation_timehack in range(0, n_days):
        # print(f'{simulation_timehack=}')
        new_infections = sim_day(population, infections[-1], simulation_timehack)
        infections[simulation_timehack] = new_infections

    # print(f'{infections=}')
    # Make sure your not modifying data when someone else is.
    lock.acquire()

    day_results[i, :] = infections
    # print(f'{day_results[i]=}')

    # Always release the lock!
    lock.release()


def main():
    np.random.seed(42)
    # Simulate many episodes

    day_results_base = mp.Array(ctypes.c_double, eps * n_days)

    pool = mp.Pool(processes=mp.cpu_count(), initializer=init, initargs=(day_results_base,))
    pool.map(episode, range(eps))
    # pool.close()

    day_results = np.ctypeslib.as_array(day_results_base.get_obj())
    day_results = day_results.reshape(eps, n_days)
    # print(day_results)

    # Calculate and print stats

    # Average number of days epidemics lasted
    epidem_lens = np.argmax(day_results, axis=1) + 4  # Zero-index + 3 (number of days contagious) + 1
    print('Consider a pandemic complete if no infected students remain.')
    print('Mean days pandemic lasted:', epidem_lens.mean())
    print('Median days pandemic lasted:', median(epidem_lens))

    # Average number infected over all episodes
    print('Mean infections:', day_results[:, -1].mean())
    print('Median infections:', median(day_results[:, -1]))

    # Expected value of infected by each day
    expected_values = day_results.mean(axis=0)
    # n_days = 41
    expected_df = pd.DataFrame(list(range(1, n_days + 1)), columns=["Day"])
    expected_df['Mean'] = expected_values[:n_days]

    # print(expected_df)
    expected_df.to_csv(data_dir / f'Flu_Pandemic_{eps}_weekend_{weekend_check}.csv', index=False)

    title = f'Histogram of Days the Epidemic Lasted\n {eps:,} Episodes. Mean = {round(epidem_lens.mean(), 2)} days, Median = {median(epidem_lens)} days'
    plt.hist(epidem_lens)
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Episodes')
    plt.savefig(fig_dir / f'Flu_Pandemic_Fig1_{eps}_weekend_{weekend_check}.png')
    # plt.show()

    title = f'Histogram of Days the Epidemic Lasted\n {eps:,} Episodes. Mean = {round(epidem_lens.mean(), 2)} days, Median = {median(epidem_lens)} days'
    plt.hist(epidem_lens, bins=range(min(epidem_lens), max(epidem_lens) + 1, 1))
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Episodes')
    plt.savefig(fig_dir / f'Flu_Pandemic_Fig1_smallbins_{eps}_weekend_{weekend_check}.png')
    # plt.show()

    title = f'Line Chart of Infections: {eps:,} Episodes.\nMean = {round(expected_df["Mean"].mean(), 2)} infections, Median = {round(median(expected_df["Mean"]), 2)} infections'

    # evaluate the histogram
    hist, bins = np.histogram(expected_df['Mean'], bins=len(expected_df['Mean']), range=[1, len(expected_df['Mean'])])
    offset = bins[1:] - bins[:-1]
    plt.plot(bins[:-1] + offset, np.cumsum(expected_df['Mean']), c='blue', label='Cumulative Infections')
    plt.plot(expected_df['Mean'], c='red', label='Daily Infections')
    plt.legend(loc='upper left', frameon=False)
    plt.grid()

    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Mean Infections')
    plt.savefig(fig_dir / f'Flu_Pandemic_means_{eps}_weekend_{weekend_check}.png')
    # plt.show()


if __name__ == "__main__":
    main()
