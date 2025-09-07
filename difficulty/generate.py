import hashlib
import time
import os
import statistics
from scipy.io import savemat
import csv

def mine(target):
    start_time = time.time()
    attempts = 0
    while True:
        random_input = os.urandom(32)  # Generate random input
        h = hashlib.sha256(random_input).hexdigest()
        difficulty = calculate_difficulty(h)
        attempts += 1
        if difficulty >= target:
            return time.time() - start_time, attempts

def calculate_difficulty(hash_hex):
    hash_binary = bin(int(hash_hex, 16))[2:].zfill(256)
    leading_zeros = len(hash_binary) - len(hash_binary.lstrip('0'))
    return 2**leading_zeros

def process(difficulty_target):
    print(f"Starting mining process for difficulty target: {difficulty_target} leading zeros")
    times = []
    attempts = []

    runs = 1000
    while runs >= 0:
        t, a = mine(difficulty_target)
        times.append(t)
        attempts.append(a)

        if len(times) > 1:  # Need at least two data points for standard deviation
            mean_time = statistics.mean(times)

            mean_attempts = sum(attempts) / len(attempts)
            squared_deviations = [(x - mean_attempts) ** 2 for x in attempts]
            sum_squared_deviations = sum(squared_deviations)
            variance = sum_squared_deviations / len(attempts)
            sd = variance ** 0.5

            print(f"Time: {t:9.5f}, Mean: {mean_time:12.5f} s, Mean Attempts: {mean_attempts:12}, Deviation: {sd:12.5f} sigma")
            runs -= 1

    savemat('attempts.mat', {'a': attempts})
    with open('attempts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['solve_time_ms' ,'difficulty'])
        for i in range(len(attempts)):
            writer.writerow([times[i]*1000, difficulty_target])

if __name__ == "__main__":
    difficulty_target = 32768
    process(difficulty_target)
