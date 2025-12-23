import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd

# 1. Setup
# Create a folder called 'cache' in the same folder as this script first!
fastf1.Cache.enable_cache('cache')
fastf1.plotting.setup_mpl(misc_mpl_mods=False) # Make the plot look like F1 style

# 2. Load the Race
print("Loading Bahrain 2023 Race Data... (This takes 1-2 mins)")
session = fastf1.get_session(2023, 'Bahrain', 'R')
session.load()

# 3. Pick the Driver (Verstappen)
driver = 'VER'
laps = session.laps.pick_driver(driver)

# 4. Filter the Data (CRITICAL STEP)
# We only want "racing" laps. Not pit stops, not safety car laps.
# Logic: If the lap is more than 105% of the fastest lap, it's likely a pit stop/slow lap.
fastest_lap_time = laps.pick_fastest()['LapTime']
threshold = fastest_lap_time * 1.05
racing_laps = laps[laps['LapTime'] < threshold]

# 5. Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Convert LapTime to seconds for the Y-axis so it plots correctly
# We use .dt.total_seconds() to make it a number
ax.plot(racing_laps['LapNumber'], racing_laps['LapTime'].dt.total_seconds(),
        marker='o', linestyle='-', color='red', label='VER Lap Times')

ax.set_title(f'{driver} Lap Times - Bahrain 2023 (Tire Wear Check)')
ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time (Seconds)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.show()