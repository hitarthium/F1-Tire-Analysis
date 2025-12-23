import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 1. Setup
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

fastf1.Cache.enable_cache(cache_dir) 
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# 2. Load the Race
print("Loading Bahrain 2023 Race Data...")
session = fastf1.get_session(2023, 'Bahrain', 'R')
session.load()

# --- THE COMPARISON FUNCTION ---
def analyze_driver(driver_code, color):
    print(f"Analyzing {driver_code}...")
    
    # Get Laps
    laps = session.laps.pick_driver(driver_code)
    
    # Smart Filter (Remove Outliers)
    mean_lap = laps['LapTime'].dt.total_seconds().mean()
    std_lap = laps['LapTime'].dt.total_seconds().std()
    upper_limit = mean_lap + (2.0 * std_lap)
    lower_limit = mean_lap - (2.0 * std_lap)
    
    clean_laps = laps[
        (laps['LapTime'].dt.total_seconds() < upper_limit) & 
        (laps['LapTime'].dt.total_seconds() > lower_limit)
    ]
    
    # Calculate Wear
    x = clean_laps['LapNumber']
    y = clean_laps['LapTime'].dt.total_seconds()
    
    # Polyfit returns [slope, intercept]
    slope, intercept = np.polyfit(x, y, 1)
    
    # Fuel Correction (+0.05s/lap)
    fuel_correction = 0.05
    true_wear = slope + fuel_correction
    
    return x, y, slope, intercept, true_wear

# 3. Analyze Both Drivers
# We run the function twice!
ver_x, ver_y, ver_slope, ver_int, ver_wear = analyze_driver('VER', 'red')
per_x, per_y, per_slope, per_int, per_wear = analyze_driver('PER', 'blue')

# 4. Print the "Winner"
print(f"\n--- BATTLE RESULTS (Lower is Better) ---")
print(f"VER True Wear: +{ver_wear:.4f} s/lap")
print(f"PER True Wear: +{per_wear:.4f} s/lap")
diff = per_wear - ver_wear
print(f"Difference:    {abs(diff):.4f} s/lap")
if ver_wear < per_wear:
    print(f"WINNER: VERSTAPPEN (Saved tires better)")
else:
    print(f"WINNER: PEREZ (Saved tires better)")
print(f"----------------------------------------")

# 5. Plot the Battle
fig, ax = plt.subplots(figsize=(12, 7))

# Plot Verstappen (Red)
ax.scatter(ver_x, ver_y, color='red', label='VER Laps', alpha=0.6)
ax.plot(ver_x, ver_slope*ver_x + ver_int, color='darkred', linestyle='--', linewidth=2, label=f'VER Wear: +{ver_wear:.3f}')

# Plot Perez (Blue)
ax.scatter(per_x, per_y, color='blue', label='PER Laps', alpha=0.6)
ax.plot(per_x, per_slope*per_x + per_int, color='navy', linestyle='--', linewidth=2, label=f'PER Wear: +{per_wear:.3f}')

ax.set_title(f'Tire Wear Battle: VER vs PER (Bahrain 2023)')
ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time (Seconds)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.show()