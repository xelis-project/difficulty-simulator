import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Constants
COIN_VALUE = int(1e8)
MAXIMUM_SUPPLY = 18_400_000 * COIN_VALUE
EMISSION_SPEED_FACTOR = 20
# Show it on a year basis
TIME_FRAME = 24 * 60 * 60 * 365
# estimate daily production
BLOCK_TIME = 60 * 60 * 24

# Reward calculation
def get_block_reward(supply):
    if supply >= MAXIMUM_SUPPLY:
        return 0
    base_reward = (MAXIMUM_SUPPLY - supply) >> EMISSION_SPEED_FACTOR
    return base_reward * BLOCK_TIME // 180

# Simulation
supply = 0
times = []
supplies = []
current_time = 0

while supply < MAXIMUM_SUPPLY and len(times) < 30:
    reward = get_block_reward(supply)
    if reward == 0:
        break

    supply += reward
    current_time += BLOCK_TIME

    # record supply at each full year
    if len(times) == 0 or current_time % TIME_FRAME == BLOCK_TIME:
        times.append(current_time / TIME_FRAME)
        supplies.append(supply/COIN_VALUE)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(times, supplies, label="Estimated Supply")
plt.axhline(MAXIMUM_SUPPLY/COIN_VALUE, color="red", linestyle="--", label="Max Supply")
plt.xlabel("Years")
plt.ylabel("Supply (millions)")
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{(x/1_000_000.0):.2f}")
)
plt.title("Estimated Circulating Supply per Year")
plt.legend()
plt.grid(True)
plt.show()
