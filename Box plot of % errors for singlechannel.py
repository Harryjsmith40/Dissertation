import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data extracted from your provided image
data = {
    "Slot": list(range(1, 25)),
    "Programmed Volume (µL)": [
        40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600,
        640, 680, 720, 760, 800, 840, 880, 920, 960
    ],
    "Volume Dispensed (µL)": [
        37.0, 76.0, 120.0, 163.0, 200.0, 243.0, 283.0, 322.0, 362.0, 403.0, 484.0,
        484.0, 527.0, 560.0, 606.0, 642.0, 685.0, 723.0, 766.0, 806.0, 842.0, 883.0,
        925.0, 955.0
    ],
    "Error (µL)": [
        3.0, 4.0, 0.0, 3.0, 0.0, 3.0, 3.0, 2.0, 2.0, 3.0, 4.0, 4.0, 7.0, 0.0, 6.0,
        2.0, 5.0, 3.0, 6.0, 6.0, 2.0, 3.0, 5.0, 5.0
    ],
    "% Error": [
        7.5, 5.0, 0.0, 1.875, 0.0, 1.25, 1.0714, 0.625, 0.5556, 0.75, 0.8333,
        0.8333, 1.3462, 0.0, 1.0, 0.3125, 0.7353, 0.4167, 0.7895, 0.75, 0.2381,
        0.3409, 0.5435, 0.5208
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Remove the first, second, and fourth data points
df = df.drop([0, 1, 3]).reset_index(drop=True)

# Plot: Box Plot of % Error Distribution
plt.figure(figsize=(8, 5))
sns.boxplot(df["% Error"], color="skyblue")
plt.title("Box Plot of % Error Distribution (Specific Points Removed)")
plt.xlabel("% Error")
plt.show()
