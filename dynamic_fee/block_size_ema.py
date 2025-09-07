import numpy as np
import matplotlib.pyplot as plt

# Parameters
ALPHA_VALUES = [0.05, 0.07, 0.09]
BLOCKS_COUNT = 100
MAX_BLOCK_SIZE = 1.25 * 1024 * 1024
# EMPTY_BLOCK_SIZE = 124.0

# Simulate EMA for each alpha
results = {}
for alpha in ALPHA_VALUES:
    ema_values = []
    ema = 0.0
    for i in range(BLOCKS_COUNT):
        ema = alpha * MAX_BLOCK_SIZE + (1 - alpha) * ema
        ema_values.append(ema)
    results[alpha] = ema_values

# Plot
plt.figure(figsize=(10, 6))
for alpha, values in results.items():
    plt.plot(values, label=f"EMA α={alpha}")

plt.axhline(MAX_BLOCK_SIZE, color="red", linestyle="--", label="Full block size")
plt.xlabel("Block number")
plt.ylabel("EMA value")
plt.title("EMA response with α=[0.05, 0.07, 0.09]")
plt.legend()
plt.grid(True)
plt.show()