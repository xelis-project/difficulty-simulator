import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


MAX_BLOCKS = 100_000
TARGET_BLOCK_TIME = 15 # seconds
SHIFT = 32
PROCESS_NOISE_COVAR = int(0.001 * (1<<SHIFT))
# Initial filter parameters
#x_est_prev = 5e3 # Initial hashrate estimate, maybe start with something more realistic
x_est_prev = -1
P_prev = int(0.1 * (1<<SHIFT))  # Initial estimate covariance

def filtfilt(data, window_size):
    window = np.ones(window_size) / window_size
    forward_pass = np.convolve(data, window, 'valid')
    backward_pass = np.convolve(forward_pass[::-1], window, 'valid')
    return backward_pass[::-1]

def kalman_filter_int(z, x_est_prev, P_prev):
    """
    :param z: The observed value (latest hashrate calculated on current block time).
    :param x_est_prev: The previous hashrate estimate.
    :param P_prev: The previous estimate covariance.
    :return: Updated state estimate, covariance
    """
    # scale up
    z = int(z * (1 << SHIFT))
    R = z * 2
    x_est_prev = int(x_est_prev * (1 << SHIFT))

    # Prediction step
    P_pred = P_prev + ((x_est_prev * PROCESS_NOISE_COVAR) >> SHIFT)

    # Update step
    K = (P_pred << SHIFT) // (P_pred + R)
    # ensure positive numbers only
    if z >= x_est_prev:
        x_est_new = x_est_prev + ((K * (z - x_est_prev)) >> SHIFT)
    else:
        x_est_new = x_est_prev - ((K * (x_est_prev - z)) >> SHIFT)

    P_new = (((1<<SHIFT) - K) * P_pred) >> SHIFT

    # scale down
    x_est_new = x_est_new >> SHIFT

    return x_est_new, P_new

# load data
df = pd.read_csv('attempts.csv')

# Simulation parameters
difficulty = 1e6    # starting difficulty

# Additional lists to store data for plotting
difficulties = []
estimated_hashrates = []
observed_hashrates = []
observed_blocktimes = []

for i, row in df.iterrows():
    if i >= MAX_BLOCKS:
        break

    if row['solve_time_ms'] == 0:
        continue

    difficulty = row['difficulty']
    difficulties.append(difficulty/TARGET_BLOCK_TIME)

    observed_blocktime = row['solve_time_ms'] / 1000 # to seconds
    observed_blocktimes.append(observed_blocktime)

    observed_hashrate = difficulty / observed_blocktime
    observed_hashrates.append(observed_hashrate)

    # Update the hashrate estimate using the Kalman filter
    if x_est_prev < 0:
        x_est_prev = observed_hashrate
    x_est_prev, P_prev = kalman_filter_int(
        observed_hashrate, x_est_prev, P_prev
    )
    estimated_hashrate = x_est_prev
    estimated_hashrates.append(estimated_hashrate)

    print(f"{i}: Diff: {difficulty}, Estimate: {x_est_prev}, block_blocktime = {observed_blocktime}")

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 6))
color = 'tab:red'

ax1.set_xlabel('Block Number')
ax1.set_ylabel('Hashrate / Difficulty', color='tab:orange')
# ax1.plot(difficulties, label='Difficulty', linestyle='-', color='tab:green')
# ax1.plot(filtfilt(observed_hashrates, 2), label='Observed hashrate', linestyle='-', color='tab:orange')
# ax1.plot(observed_hashrates, label='Observed hashrate', linestyle='-', color='tab:orange')
# ax1.plot(estimated_hashrates, label='Estimated hashrate', linestyle='-', color='tab:blue')
ax1.tick_params(axis='y', labelcolor=color)
# ax1.set_ylim(0, 1e8)

# Instantiate a second axes that shares the same x-axis
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Block time', color=color)  # We already handled the x-label with ax1
ax2.plot(observed_blocktimes, label='Observed block blocktime', linestyle='-', color=color)
ax2.plot(filtfilt(observed_blocktimes, 100), label='Average blocktime', linestyle='-', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:blue')
# ax2.set_ylim(0, 50)

# Added a line to make the legend combine both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

fig.tight_layout()  # To make sure layout is nicely arranged
plt.title('Block time and Hashrate Over Time')
plt.show()
