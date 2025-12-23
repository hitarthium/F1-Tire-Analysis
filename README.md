# F1 Tire Degradation Analyzer (Bahrain 2023)

## Project Overview
This project uses Python and Machine Learning to analyze Formula 1 telemetry data. By isolating tire degradation from fuel-load effects, it determines the *true* tire wear rate of drivers.

## Key Findings (Bahrain 2023)
Analyzing the "Battle of the Bulls" (Verstappen vs. Perez):
* **Max Verstappen:** High degradation (+0.024 s/lap).
* **Sergio Perez:** Minimal degradation (+0.003 s/lap).
* **Conclusion:** Perez managed tire life 8x better than Verstappen in this stint, challenging the narrative that raw speed is the only metric for success.

## Tech Stack
* **Language:** Python
* **Libraries:** FastF1, Pandas, NumPy, Matplotlib
* **Technique:** Linear Regression (Polyfit) & Statistical Outlier Rejection

## How to Run
```bash
pip install fastf1 pandas matplotlib
python tire_check.py
```
