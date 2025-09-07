import numpy as np
import matplotlib.pyplot as plt

FEE_PER_KB = 10_000.0
K = 10.0
# With EXP = 3 it ~ double base fee around 50% of block usage
EXP = 2.0

usage = np.linspace(0.0, 1.0, 100)
fee = FEE_PER_KB * (1.0 + K * np.power(usage, EXP))

plt.figure(figsize=(10,6))
plt.plot(usage * 100, fee, linewidth=2)
plt.xlabel("EMA Block usage (%)")
plt.ylabel("Base fee per KB (atomic units)")
plt.title("Smooth exponential fee curve (k=10, exp=2)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()