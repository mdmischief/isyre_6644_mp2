import numpy as np
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from scipy.stats import norm

data_dir = pathlib.Path.cwd() / 'data'
data_dir.mkdir(parents=True, exist_ok=True)

fig_dir = pathlib.Path.cwd() / 'figs'
fig_dir.mkdir(parents=True, exist_ok=True)

expected_df = pd.read_csv(data_dir / 'Flu_Pandemic_10000_weekend_True.csv')

eps=10000
weekend_check=True

# evaluate the histogram
hist, bins = np.histogram(expected_df['Mean'], bins=len(expected_df['Mean']), range=[1, len(expected_df['Mean'])])
offset = bins[1:] - bins[:-1]
plt.plot(bins[:-1] + offset, np.cumsum(expected_df['Mean']), c='blue', label='Cumulative Infections')
plt.plot(expected_df['Mean'], c='red', label='Daily Infections')
plt.legend(loc='upper left', frameon=False)
plt.grid()


title = f'Line Chart of Infections: {eps:,} Episodes.\nMean = 26.6 infections, Median = 22.0 infections'

plt.title(title)
plt.xlabel('Days')
plt.ylabel('Mean Infections')
# plt.savefig(fig_dir / f'Flu_Pandemic_means_{eps}_weekend_{weekend_check}.png')
plt.show()